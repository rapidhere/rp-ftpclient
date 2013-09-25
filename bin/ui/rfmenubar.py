#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from bin import exp, env


class MenuBar(gtk.MenuBar):
    def __init__(self, conf):
        gtk.MenuBar.__init__(self)

        self._build_up_menu(self, conf)

        self.show_all()

    @staticmethod
    def _build_up_menu(container, conf):
        for item in conf:
            if not item:
                # This is a separator
                container.append(gtk.SeparatorMenuItem())
            elif type(item) == list:
                # This is a menu item
                mi = gtk.MenuItem(item[0])
                if item[1]:
                    mi.connect("activate", item[1])
                container.append(mi)
            elif type(item) == tuple:
                # This is a submenu
                mi = gtk.MenuItem(item[0])
                submenu = gtk.Menu()
                MenuBar._build_up_menu(submenu, item[1:])
                mi.set_submenu(submenu)
                container.append(mi)