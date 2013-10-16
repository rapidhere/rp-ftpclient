#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from bin import env


class Window(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        # General Init
        self.set_default_size(*env.DEFAULT_WIN_SIZE)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title(env.WIN_TITLE)


_window_instance = None


def get_window():
    global _window_instance
    if not _window_instance:
        _window_instance = Window()

    return _window_instance