#!/usr/bin/python
#-*- coding:utf-8 -*-
import pygtk
pygtk.require("2.0")
import gobject

from filenode import FileNode


class DirectoryTreeNode(gobject.GObject):
    def __init__(self, fn=None, parent=None):
        gobject.GObject.__init__(self)

        if not fn:
            self.filenode = FileNode()
        else:
            self.filenode = fn

        self.parent = parent
        self.child_list = []

    def get_path_tuple(self):
        ret = []
        iter = self
        while iter.get_parent():
            ret = [iter.get_parent().child_list.index(iter)] + ret
            iter = iter.get_parent()

        return ret

    def get_dir_tuple(self):
        ret = []
        iter = self
        while iter.get_parent():
            ret = [iter.filenode.get_name()] + ret
            iter = iter.get_parent()

        return ret

    def is_expanded(self):
        if not hasattr(self, "_expanded") or not self._expanded:
            return False
        return True

    def set_expanded(self):
        self._expanded = True

    def set_filenode(self, fn):
        self.filenode = fn

    def get_child_list(self):
        return self.child_list

    def get_filenode(self):
        return self.filenode

    def get_nth_child(self, index):
        return self.child_list[int(index)]

    def get_n_children(self):
        return len(self.child_list)

    def get_parent(self):
        return self.parent

    def append_child(self, ch):
        self.child_list.append(ch)
        return ch

    def append_child_fn(self, fn):
        ch = DirectoryTreeNode(fn, parent=self)
        return self.append_child(ch)

    def prepend_child(self, ch):
        self.child_list = [ch] + self.child_list
        return ch

    def prepend_child_fn(self, fn):
        ch = DirectoryTreeNode(fn, parent=self)
        return self.prepend_child(ch)

    def insert_child(self, index, ch):
        self.child_list.insert(index, ch)
        return ch

    def insert_child_fn(self, index, fn):
        ch = DirectoryTreeNode(fn, parent=self)
        return self.insert_child(index, ch)

    def remove_child(self, index):
        return self.child_list.pop(index)

    def change_child(self, index, new_ch):
        self.child_list[index] = new_ch
        return new_ch

    def change_child_fn(self, index, fn):
        ch = DirectoryTreeNode(fn, parent=self)
        return self.change_child(index, ch)

    def index_child(self, node):
        index = 0
        for nd in self.child_list:
            if nd.get_filenode().get_name() == node.get_filenode().get_name():
                return index

            index += 1
        return -1