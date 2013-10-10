#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from bin import env
from bin.utils.decs import scrollable_widget
from bin.widget import get_directory_tree
from bin.widget import tree_dir_string_to_path


@scrollable_widget
class FileView(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

        self._set_up_columns()
        self.set_size_request(env.FILE_VIEW_WIDTH, env.FILE_VIEW_HEIGHT)
        self.set_rules_hint(True)
        self.show_all()

        dir_tree = get_directory_tree()
        dir_tree.connect("rf-directory-tree-add-node", self._on_dt_add_node)
        dir_tree.connect("rf-directory-tree-remove-node", self._on_dt_remove_node)
        dir_tree.connect("rf-directory-tree-change-node", self._on_dt_change_node)
        dir_tree.connect("rf-directory-tree-current-node-changed", self._on_dt_curnode_changed)

    def _on_dt_add_node(self, widget, path):
        path = tree_dir_string_to_path(path)
        dir_tree = get_directory_tree()
        cur_node = dir_tree.get_cur_node()
        node = dir_tree.get_node(path)

        if dir_tree.is_under_current_dir(node):
            index = cur_node.index_child(node)
            self.get_model().insert(index, node.get_filenode().to_list())

    def _on_dt_remove_node(self, widget, path):
        path = tree_dir_string_to_path(path)
        dir_tree = get_directory_tree()
        cur_node = dir_tree.get_cur_node()
        node = dir_tree.get_node(path)

        if dir_tree.is_under_current_dir(node):
            index = cur_node.index_child(node)
            model = self.get_model()
            model.remove(model.get_iter((index,)))
        elif dir_tree.is_on_current_dir_path(node):
            self.get_model().clear()

    def _on_dt_change_node(self, widget, path):
        path = tree_dir_string_to_path(path)
        dir_tree = get_directory_tree()
        cur_node = dir_tree.get_cur_node()
        node = dir_tree.get_node(path)

        if dir_tree.is_under_current_dir(node):
            index = cur_node.index_child(node)
            model = self.get_model()
            ch_iter = model.get_iter((index,))
            val_list = node.get_filenode().to_list()
            for ind in range(0, len(val_list)):
                model.set_value(ch_iter, ind, val_list[ind])
        elif dir_tree.is_on_current_dir_path(node):
            self.get_model().clear()

    def _on_dt_curnode_changed(self, widget, path):
        path = tree_dir_string_to_path(path)
        dir_tree = get_directory_tree()
        cur_node = dir_tree.get_node(path)

        model = self.get_model()
        model.clear()

        for ind in range(0, cur_node.get_n_children()):
            fn = cur_node.get_nth_child(ind).get_filenode()
            model.append(fn.to_list())

    def _set_up_columns(self):
        # name(icon, string)      size        date        time
        list_model = gtk.ListStore(str, str, str, str, str)
        self.set_model(list_model)

        # TreeView Column name
        tv = gtk.TreeViewColumn("Name")

        pb = gtk.CellRendererPixbuf()
        tv.pack_start(pb, False)
        tv.set_attributes(pb, stock_id=0)

        tx = gtk.CellRendererText()
        tv.pack_start(tx, True)
        tv.set_attributes(tx, text=1)

        tv.set_min_width(150)
        self.append_column(tv)

        # TreeView Column size
        tv = gtk.TreeViewColumn("Size", gtk.CellRendererText(), text=2)

        tv.set_min_width(50)
        self.append_column(tv)

        # TreeView Column date
        tv = gtk.TreeViewColumn("Date", gtk.CellRendererText(), text=3)

        tv.set_min_width(50)
        self.append_column(tv)

        # TreeView Column time
        tv = gtk.TreeViewColumn("Time", gtk.CellRendererText(), text=4)

        tv.set_min_width(50)
        self.append_column(tv)