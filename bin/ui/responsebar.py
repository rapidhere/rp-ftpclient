#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import pango

from bin import env
from bin.utils.decs import scrollable_widget

@scrollable_widget
class ResponseBar(gtk.TextView):
    def __init__(self):
        gtk.TextView.__init__(self)

        # Set up text_view
        self.set_editable(False)
        self.set_left_margin(5)
        self.set_cursor_visible(False)
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(env.RESP_BAR_BACKGROUND_COLOR))
        self.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color(env.RESP_BAR_FONT_COLOR))
        self.modify_font(pango.FontDescription(env.RESP_BAR_FONT))

        self.show()

    def append(self, txt):
        buffer = self.get_buffer()
        buffer.insert(buffer.get_end_iter(), txt)

    def append_line(self, txt):
        self.append(txt + "\n")