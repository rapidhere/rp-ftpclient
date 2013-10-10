#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gobject

from bin import exp, env
from bin.utils.decs import scrollable_widget
from bin.widget import get_directory_tree


@scrollable_widget
class DirectoryView(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

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

    def _on_dt_add_node(self, widget, path):
        pass

    def _on_dt_remove_node(self, widget, path):
        pass

    def _on_dt_change_node(self, widget, path):
        pass

    def _on_dt_curnode_changed(self, widget, path):
        pass


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
        pass

    def on_get_path(self, iter):
        pass

    def on_get_value(self, iter, column):
        pass

    def on_iter_next(self, iter):
        pass

    def on_iter_children(self, iter):
        pass

    def on_iter_has_child(self, iter):
        pass

    def on_iter_n_children(self, iter):
        pass

    def on_iter_nth_child(self, iter, index):
        pass

    def on_iter_parent(self, iter):
        pass

    def set_root(self, root_dir):
        pass