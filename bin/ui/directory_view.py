#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gobject

from bin.utils.decs import scrollable_widget
from bin.widget import get_directory_tree, tree_dir_path_to_string, tree_dir_string_to_path, FILE_TYPE_DIR
from utils import *


@scrollable_widget
class DirectoryView(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

        tv_model = DirectoryViewModel()
        self.set_model(tv_model)

        tv = gtk.TreeViewColumn("Directory Tree")
        pb = gtk.CellRendererPixbuf()
        tv.pack_start(pb, False)
        tv.set_attributes(pb, stock_id=1)

        tx = gtk.CellRendererText()
        tv.pack_start(tx, True)
        tv.set_attributes(tx, text=0)

        tv.set_min_width(200)
        self.append_column(tv)

        self._current_path = None

        self.set_enable_tree_lines(True)
        self.set_rules_hint(True)

        self.show_all()

        dir_tree = get_directory_tree()
        self.handler_id = {
            "add": dir_tree.connect("rf-directory-tree-add-node", self._on_dt_add_node),
            "remove": dir_tree.connect("rf-directory-tree-remove-node", self._on_dt_remove_node),
            "change": dir_tree.connect("rf-directory-tree-change-node", self._on_dt_change_node),
            "cur_changed": dir_tree.connect("rf-directory-tree-current-node-changed", self._on_dt_curnode_changed),
        }

    def _on_dt_add_node(self, widget, path):
        path = tree_dir_string_to_path(path)

        fn = get_directory_tree().get_node(path).get_filenode()
        if fn.get_type() == FILE_TYPE_DIR:
            model = self.get_model()
            path = common_path_to_dir_path(path)
            model.row_inserted(path, model.get_iter(path))

    def _on_dt_remove_node(self, widget, path):
        pass

    def _on_dt_change_node(self, widget, path):
        pass

    def _on_dt_curnode_changed(self, widget, path):
        path = tree_dir_string_to_path(path)
        node = get_directory_tree().get_node(path)
        if node.get_filenode().get_type() != FILE_TYPE_DIR:
            return

        path = common_path_to_dir_path(path)
        if path == self._current_path:
            return False

        self._current_path = path
        self.expand_to_path(path)
        self.expand_row(path, False)
        self.set_cursor_on_cell(path)

gobject.signal_new(
    "rf-dir-view-expand-node",
    DirectoryView, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_BOOLEAN,
    (gobject.TYPE_STRING,)
)

gobject.signal_new(
    "rf-dir-view-activate",
    DirectoryView, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_BOOLEAN,
    (gobject.TYPE_STRING,)
)

_directory_view_instance = None


def get_directory_view():
    global _directory_view_instance
    if not _directory_view_instance:
        _directory_view_instance = DirectoryView()

        def _on_dvmodel_expand_node(widget, path):
            _directory_view_instance.emit("rf-dir-view-expand-node", path)

        _directory_view_instance.get_model().connect("rf-dvmodel-expand-iter", _on_dvmodel_expand_node)

        def _on_row_activated(widget, path, column):
            c_path = dir_path_to_common_path(path)
            _directory_view_instance.emit("rf-dir-view-activate", tree_dir_path_to_string(c_path))

        _directory_view_instance._inner.connect("row-activated", _on_row_activated)

    return _directory_view_instance


class DirectoryViewModel(gtk.GenericTreeModel):
    column_type = (str, str)

    def __init__(self):
        gtk.GenericTreeModel.__init__(self)

    def on_get_flags(self):
        return gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.column_type)

    def on_get_column_type(self, index):
        return self.column_type[index]

    def on_get_iter(self, path):
        try:
            ret = get_directory_tree()._root
            for ind in path:
                ret = get_nth_dir_child(ret, ind)
            return ret
        except IndexError:
            return None

    def on_get_path(self, iter):
        ret = []
        while iter.get_parent():
            ind = self.index_dir_child(iter)
            iter = iter.get_parent()
            ret = [ind] + ret
        return ret

    def on_get_value(self, iter, column):
        if column == 0:
            return iter.get_filenode().get_name()
        elif column == 1:
            return gtk.STOCK_DIRECTORY

    def on_iter_next(self, iter):
        try:
            index = index_dir_child(iter) + 1
            return get_nth_dir_child(iter.get_parent(), index)
        except IndexError:
            return None

    def on_iter_children(self, iter):
        if not iter:
            return get_directory_tree()._root

        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))
        return get_nth_dir_child(iter, 0)

    def on_iter_has_child(self, iter):
        if not iter:
            iter = get_directory_tree()._root

        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))
        cnt = 0
        for ch in iter.get_child_list():
            if ch.get_filenode().get_type() == FILE_TYPE_DIR:
                cnt += 1
        return cnt != 0

    def on_iter_n_children(self, iter):
        if not iter:
            iter = get_directory_tree()._root

        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))

        cnt = 0
        for ch in iter.get_child_list():
            if ch.get_filenode().get_type() == FILE_TYPE_DIR:
                cnt += 1
        return cnt

    def on_iter_nth_child(self, iter, index):
        if not iter:
            iter = get_directory_tree()._root

        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))

        try:
            return get_nth_dir_child(iter, index)
        except IndexError:
            return None

    def on_iter_parent(self, iter):
        return iter.get_parent()

gobject.signal_new(
    "rf-dvmodel-expand-iter",
    DirectoryViewModel, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_BOOLEAN,
    (gobject.TYPE_STRING, )
)