#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk


def scrollable_widget(cls):
    class _ScrollWindowContainer(gtk.ScrolledWindow):
        def __init__(self, *args, **kwargs):
            gtk.ScrolledWindow.__init__(self)

            self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

            self._inner = cls(*args, **kwargs)
            self.add(self._inner)

            self.show_all()

        def __getattr__(self, item):
            return getattr(self._inner, item)

    return _ScrollWindowContainer