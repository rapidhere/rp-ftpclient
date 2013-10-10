#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gobject

from utils import tree_dir_path_to_string
from decs import std_path_notify_function
from directory_tree_node import DirectoryTreeNode


class DirectoryTree(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)
        self._root = DirectoryTreeNode()
        self._root.set_expanded()

    def set_cur_node(self, node):
        self.cur_node = node
        self.emit("rf-directory-tree-current-node-changed",
                  tree_dir_path_to_string(node.get_path_tuple()))

    def get_cur_node(self):
        return self.cur_node

    def set_root(self, root_fn):
        root = DirectoryTreeNode(root_fn, self._root)
        self._root.child_list = [root]
        self.set_cur_node(root)

        if self._root.get_n_children():
            self.emit("rf-directory-tree-remove-node", tree_dir_path_to_string(
                self._root.get_nth_child(0).get_path_tuple()
            ))
        self.emit("rf-directory-tree-add-node", tree_dir_path_to_string(root.get_path_tuple()))

    def get_root(self):
        return self._root.get_nth_child(0)

    def get_node(self, path):
        ret = self._root
        for ind in path:
            ret = ret.get_nth_child(ind)

        return ret

    def is_under_current_dir(self, node):
        if self.cur_node.index_child(node) == -1:
            return False
        return True

    def is_on_current_dir_path(self, node):
        path = node.get_dir_tuple()
        cur_path = self.cur_node.get_dir_tuple()
        if len(path) <= len(cur_path):
            len_path = len(path)
            for index in range(0, len_path):
                if cur_path[index] != path[index]:
                    return False
            return True
        return False

    @std_path_notify_function("rf-directory-tree-add-node")
    def append_child(self, cur_node, ch):
        return cur_node.append_child(ch)

    @std_path_notify_function("rf-directory-tree-add-node")
    def append_child_fn(self, cur_node, fn):
        return cur_node.append_child_fn(fn)

    @std_path_notify_function("rf-directory-tree-add-node")
    def prepend_child(self, cur_node, ch):
        return cur_node.prepend_child(ch)

    @std_path_notify_function("rf-directory-tree-add-node")
    def prepend_child_fn(self, cur_node, fn):
        return cur_node.prepend_child_fn(fn)

    @std_path_notify_function("rf-directory-tree-add-node")
    def insert_child(self, cur_node, index, ch):
        return cur_node.insert_child(index, ch)

    @std_path_notify_function("rf-directory-tree-add-node")
    def insert_child_fn(self, cur_node, index, fn):
        return cur_node.insert_child(index, fn)

    @std_path_notify_function("rf-directory-tree-remove-node")
    def remove_child(self, cur_node, index):
        return cur_node.remove_child(index)

    @std_path_notify_function("rf-directory-tree-change-node")
    def change_child(self, cur_node, index, new_ch):
        return cur_node.change_child(index, new_ch)

    @std_path_notify_function("rf-directory-tree-change-node")
    def change_child_fn(self, cur_node, index, new_fn):
        return cur_node.change_child_fn(index, new_fn)


_global_directory_tree_instance = None


def get_directory_tree():
    global _global_directory_tree_instance
    if not _global_directory_tree_instance:
        _global_directory_tree_instance = DirectoryTree()
    return _global_directory_tree_instance

gobject.signal_new(
    "rf-directory-tree-add-node",
    DirectoryTree, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_NONE,
    (gobject.TYPE_STRING,)
)

gobject.signal_new(
    "rf-directory-tree-remove-node",
    DirectoryTree, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_NONE,
    (gobject.TYPE_STRING,)
)

gobject.signal_new(
    "rf-directory-tree-change-node",
    DirectoryTree, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_NONE,
    (gobject.TYPE_STRING,)
)

gobject.signal_new(
    "rf-directory-tree-current-node-changed",
    DirectoryTree, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_NONE,
    (gobject.TYPE_STRING,)
)