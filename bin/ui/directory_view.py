#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gobject

from bin.utils.decs import scrollable_widget
from bin.widget import get_directory_tree, tree_dir_path_to_string, tree_dir_string_to_path, FILE_TYPE_DIR


@scrollable_widget
class DirectoryView(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

        gobject.signal_new(
            "rf-dir-view-expand-node",
            self.__class__, gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_BOOLEAN,
            (gobject.TYPE_STRING,)
        )

        tv_model = DirectoryViewModel()
        self.set_model(tv_model)

        tv = gtk.TreeViewColumn("Directory Tree", gtk.CellRendererText(), text=0)
        tv.set_min_width(200)
        self.append_column(tv)

        self._current_dir = None

        self.set_enable_tree_lines(True)
        self.set_rules_hint(True)

        self.show_all()

        dir_tree = get_directory_tree()
        dir_tree.connect("rf-directory-tree-add-node", self._on_dt_add_node)
        dir_tree.connect("rf-directory-tree-remove-node", self._on_dt_remove_node)
        dir_tree.connect("rf-directory-tree-change-node", self._on_dt_change_node)
        dir_tree.connect("rf-directory-tree-current-node-changed", self._on_dt_curnode_changed)

        tv_model.connect("rf-dvmodel-expand-iter", self._on_dvmodel_expand_node)

    def _on_dt_add_node(self, widget, path):
        path = tree_dir_string_to_path(path)

        fn = get_directory_tree().get_node(path).get_filenode()
        if fn.get_type() == FILE_TYPE_DIR:
            print "##" + fn.get_name()
            model = self.get_model()
            model.row_inserted(path, model.get_iter(path))

    def _on_dt_remove_node(self, widget, path):
        pass

    def _on_dt_change_node(self, widget, path):
        pass

    def _on_dt_curnode_changed(self, widget, path):
        pass

    def _on_dvmodel_expand_node(self, widget, path):
        return self.emit("rf-dir-view-expand-node", path)


class DirectoryViewModel(gtk.GenericTreeModel):
    column_type = (str,)

    def __init__(self):
        gtk.GenericTreeModel.__init__(self)

    def on_get_flags(self):
        return gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.column_type)

    def on_get_column_type(self, index):
        return self.column_type[index]

    def on_get_iter(self, path):
        # ret = get_directory_tree().get_root()
        # for ind in path:
        #     if len(ret.get_n_children()) == 0:
        #         self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(ret.get_path_tuple()))
        #     ret = ret.get_nth_child(ind)
        # return ret
        try:
            return get_directory_tree().get_node(path)
        except IndexError:
            return None

    def on_get_path(self, iter):
        return iter.get_path_tuple()

    def on_get_value(self, iter, column):
        if column == 0:
            return iter.get_filenode().get_name()

    def on_iter_next(self, iter):
        try:
            parent = iter.get_parent()
            index = parent.index_child(iter) + 1
            return parent.get_nth_child(index)
        except IndexError:
            return None

    def on_iter_children(self, iter):
        if not iter:
            return get_directory_tree().get_root()

        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))
        return iter.get_nth_child(0)

    def on_iter_has_child(self, iter):
        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))
        return iter.get_n_children() != 0

    def on_iter_n_children(self, iter):
        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))
        return iter.get_n_children()

    def on_iter_nth_child(self, iter, index):
        if not iter:
            return get_directory_tree().get_root().get_nth_child(index)

        if not iter.is_expanded():
            self.emit("rf-dvmodel-expand-iter", tree_dir_path_to_string(iter.get_path_tuple()))
        return iter.get_nth_child(index)

    def on_iter_parent(self, iter):
        return iter.get_parent()

gobject.signal_new(
    "rf-dvmodel-expand-iter",
    DirectoryViewModel, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_BOOLEAN,
    (gobject.TYPE_STRING, )
)