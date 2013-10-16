#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import pango
import datetime

from bin import env
from bin.utils.decs import scrollable_widget


@scrollable_widget
class ResponseView(gtk.TextView):
    def __init__(self):
        self.tag_table = gtk.TextTagTable()
        self.text_buffer = gtk.TextBuffer(self.tag_table)
        gtk.TextView.__init__(self, self.text_buffer)

        # Set up text_view
        self.set_editable(False)
        self.set_left_margin(5)
        self.set_cursor_visible(False)
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(env.RESP_VIEW_BACKGROUND_COLOR))
        self.modify_font(pango.FontDescription(env.RESP_VIEW_FONT))

        # Set up tags
        self._create_tag("tag_info", env.RESP_VIEW_INFO_FONT_COLOR)
        self._create_tag("tag_warning", env.RESP_VIEW_WARNING_FONT_COLOR)
        self._create_tag("tag_error", env.RESP_VIEW_ERROR_FONT_COLOR)
        self._create_tag("tag_client", env.RESP_VIEW_SEND_CMD_FONT_COLOR)
        self._create_tag('tag_server', env.RESP_VIEW_SERVER_RESP_FONT_COLOR)

        self.show()

    def _create_tag(self, tag_name, color):
        tag = gtk.TextTag()
        tag.set_property("foreground-gdk", gtk.gdk.color_parse(color))
        setattr(self, tag_name, tag)
        self.tag_table.add(tag)

    def append_info(self, txt, indent=0):
        self.append(txt, indent, self.tag_info)

    def append_warning(self, txt, indent=0):
        self.append(txt, indent, self.tag_warning)

    def append_error(self, txt, indent=0):
        self.append(txt, indent, self.tag_error)

    def append_info_line(self, txt):
        if not txt[:-1] == '\n':
            txt += '\n'
        self.append_info(txt)

    def append_warning_line(self, txt):
        if not txt[:-1] == '\n':
            txt += '\n'
        self.append_warning(txt)

    def append_error_line(self, txt):
        if not txt[:-1] == '\n':
            txt += '\n'
        self.append_error(txt)

    def append_send_cmd_info(self, cmd):
        t = datetime.datetime.now()
        self.append("[Client] at %s " % t.time().strftime("%S.%f"), 1, self.tag_client)
        self.append_info_line(cmd)

    def append_server_resp(self, resp, tag):
        t = datetime.datetime.now()
        self.append("[Server] at %s " % t.time().strftime("%S.%f"), 1, self.tag_server)
        self.append(repr(resp) + "\n", 0, tag)

    def append_server_resp_info(self, resp):
        self.append_server_resp(resp, self.tag_info)

    def append_server_resp_warning(self, resp):
        self.append_server_resp(resp, self.tag_warning)

    def append_server_resp_error(self, resp):
        self.append_server_resp(resp, self.tag_error)

    def append(self, txt, indent, tag):
        txt = indent * 4 * " " + txt

        buffer = self.text_buffer
        buffer.insert_with_tags(buffer.get_end_iter(), txt, tag)

        mark = buffer.get_mark("insert")
        self.scroll_to_mark(mark, 0.0)

        if self.text_buffer.get_line_count() > env.RESP_VIEW_MAX_LINE:
            n_line = self.text_buffer.get_line_count() - env.RESP_VIEW_MAX_LINE
            iter = self.text_buffer.get_start_iter()
            for i in range(0, n_line):
                iter.forward_line()
            self.text_buffer.delete(self.text_buffer.get_start_iter(), iter)


def get_response_view():
    return ResponseView()