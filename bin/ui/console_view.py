#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import pango
import gobject

from bin.utils.decs import scrollable_widget
from bin import env
from bin.widget import get_cmd_parser
from bin import exp
from rfwindow import get_window
from bin.net import get_ftp
from bin.widget import get_directory_tree, FileNode, FILE_TYPE_DIR

@scrollable_widget
class ConsoleView(gtk.TextView):
    def __init__(self):
        gtk.TextView.__init__(self)

        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color(env.CONSOLE_VIEW_BGCOLOR))
        self.modify_text(gtk.STATE_NORMAL, gtk.gdk.Color(env.CONSOLE_VIEW_FGCOLOR_NORMAL))
        self.modify_font(pango.FontDescription(env.CONSOLE_VIEW_FONT))

        self.connect("key-press-event", self._on_key_press)
        self.connect("button-press-event", self._on_button_press)

        self._append_new_text("rp-ftp-client Console ver 0.1")
        self._start_new_line()

    def _start_new_line(self):
        self._buffer = []
        self._pos = 0

        self._append_new_text("\n" + env.CONSOLE_VIEW_PROMPT)

    def _append_new_text(self, txt):
        if not txt:
            txt = ''

        buffer = self.get_buffer()
        buffer.insert(buffer.get_end_iter(), txt)

        mark = buffer.get_mark("insert")
        self.scroll_to_mark(mark, 0.0)

        if buffer.get_line_count() > env.CONSOLE_VIEW_MAX_LINE:
            n_line = buffer.get_line_count() - env.RESP_VIEW_MAX_LINE
            iter = buffer.get_start_iter()
            for i in range(0, n_line):
                iter.forward_line()
            buffer.delete(buffer.get_start_iter(), iter)

    def _on_button_press(self, widget, event, data=None):
        return True

    def _on_key_press(self, widget, event, data=None):
            key = gtk.gdk.keyval_name(event.keyval)
            if key == "Up":
                return True
            elif key == "Down":
                return True
            elif key == 'Left':
                if self._pos:
                    self._pos -= 1
                else:
                    return True
            elif key == 'Right':
                if self._pos < len(self._buffer):
                    self._pos += 1
                else:
                    return True
            elif key == 'BackSpace':
                if self._pos:
                    self._buffer.pop(self._pos - 1)
                    self._pos -= 1
                else:
                    return True
            elif key == 'Return':
                flag = False
                for ch in self._buffer:
                    if ch != ' ':
                        flag = True
                if flag:
                    ret = self._on_cmd()
                    if ret:
                        self._append_new_text("\n" + ret)
                self._start_new_line()
                return True
            elif key == 'Tab':
                return True
            else:
                key = gtk.gdk.keyval_to_unicode(event.keyval)
                if key < 255 and key:
                    self._buffer.insert(self._pos, chr(key))
                    self._pos += 1

            return False

    def _on_cmd(self):
        cmd = "".join(self._buffer)

        try:
            cmd_name, pars = get_cmd_parser().parse_cmd_line(cmd)
        except exp.CMDException as e:
            return str(e)

        return getattr(self, "_on_cmd_" + cmd_name)(**pars)

    def _require_login(func):
        def _func(self, *args, **kwargs):
            if get_ftp().is_login():
                return func(self, *args, **kwargs)

            return "Must login in first!"

        return _func

    def _on_cmd_quit(self):
        get_window().destroy()
        return "Quiting ..."

    @_require_login
    def _on_cmd_ls(self):
        return get_ftp().list_current_dir()

    @_require_login
    def _on_cmd_cd(self, dir):
        try:
            get_directory_tree().change_into_child(dir)
        except exp.DirectoryTreeChangeIntoChildFailed as e:
            return str(e)

    @_require_login
    def _on_cmd_cdup(self):
        try:
            get_directory_tree().change_into_parent()
        except exp.DirectoryTreeChangeIntoParentFailed as e:
            return str(e)

    def _on_cmd_connect(self, host, port):
        if port:
            get_ftp().connect_to_host(host, port)
        else:
            get_ftp().connect_to_host(host)

    def _on_cmd_login(self, usr, psw, act):
        try:
            get_ftp().login(usr, psw, act)

            root_dir = get_ftp().print_current_dir()
            root_fn = FileNode(name=root_dir, type=FILE_TYPE_DIR)
            get_directory_tree().set_root(root_fn)
        except Exception:
            return "Login failed"

    @_require_login
    def _on_cmd_pwd(self):
        return get_ftp().print_current_dir()

    def _on_cmd_clear(self):
        self.get_buffer().set_text("rp-ftp-client Console ver 0.1")


_console_view_instance = None


def get_console_view():
    global _console_view_instance
    if not _console_view_instance:
        _console_view_instance = ConsoleView()

    return _console_view_instance