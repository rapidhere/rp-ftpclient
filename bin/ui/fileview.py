#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from bin import env, exp
from bin.utils.decs import scrollable_widget


@scrollable_widget
class FileView(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)

        self._set_up_columns()
        self.set_size_request(0, env.FILE_VIEW_HEIGHT)
        self.set_rules_hint(True)
        self.show_all()

    def _set_up_columns(self):
        index = 0
        for conf in env.FILE_VIEW_COLUMN_CONFIG:
            col = gtk.TreeViewColumn(conf[0], gtk.CellRendererText(), text=index)
            col.set_resizable(True)
            col.set_min_width(conf[1])
            self.append_column(col)
            index += 1
        store = gtk.ListStore(*env.FILE_VIEW_COLUMN_TYPE_CONFIG)
        self.set_model(store)

    def prepend(self, filenode):
        self.get_model().prepend(filenode.to_list())

    def append(self, filenode):
        self.get_model().append(filenode.to_list())

    def clear(self):
        self.get_model().clear()