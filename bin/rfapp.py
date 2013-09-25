#!/usr/bin/python
#-*- coding :utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from bin.ui import Window, MenuBar, FileView, ResponseBar
from bin.ui.dialogs import BaseConnectDialog, BASE_CONNECT_DIA_BT_CONNECT, BASE_CONNECT_DIA_BT_CANCEL
from bin import env


class RFApp:
    def __init__(self):
        self.win = Window(self)
        self._load_up_menubar()
        self._load_up_file_list_view()
        self._load_up_resp_bar()

        # Set up layout
        vbox = gtk.VBox(False)
        vbox.pack_start(self.menubar, False, False)

        paned = gtk.VPaned()
        paned.add1(self.file_view)
        paned.add2(self.resp_bar)
        paned.show()
        vbox.pack_start(paned, True, True)

        vbox.show()
        self.win.add(vbox)

        # Connect signals
        self.win.connect("destroy", lambda w: self.exit())

        self.win.show()

    def run(self):
        gtk.main()

    def _load_up_menubar(self):
        MENU_BAR_CONF = (
            (
                "_connect",
                ["_base connect", self._on_menubar_base_connect],
                ["_advanced connect", self._on_menubar_advanced_connect],
                None,
                ["_history", self._on_menubar_history]
            ),
            (
                "_options",
                ["_general options", self._on_menubar_general_options],
                None,
                ["_advanced options", self._on_menubar_advanced_options],
            ),
            (
                "_help",
                ["_help", self._on_menubar_help],
                None,
                ["_about", self._on_menubar_about],
            ),
        )

        self.menubar = MenuBar(MENU_BAR_CONF)

    def _load_up_file_list_view(self):
        self.file_view = FileView()

    def _load_up_resp_bar(self):
        self.resp_bar = ResponseBar()

        self.resp_bar.append_line(env.RESP_BAR_WELCOME_INFO)

    def _on_menubar_base_connect(self, widget, data=None):
        dia = BaseConnectDialog(self.win)
        resp = dia.run()

        if resp.resp_id == BASE_CONNECT_DIA_BT_CONNECT:
            print resp.resp_id
            print resp.hst
            print resp.usr
            print resp.pss
        elif resp.resp_id == BASE_CONNECT_DIA_BT_CANCEL:
            pass

    def _on_menubar_advanced_connect(self, widget, data=None):
        pass

    def _on_menubar_history(self, widget, data=None):
        pass

    def _on_menubar_general_options(self, widget, data=None):
        pass

    def _on_menubar_advanced_options(self, widget, data=None):
        pass

    def _on_menubar_help(self, widget, data=None):
        pass

    def _on_menubar_about(self, widget, data=None):
        pass

    def exit(self):
        gtk.main_quit()

# Global App instance
_app_instance = None


def get_app():
    global _app_instance
    if not _app_instance:
        _app_instance = RFApp()
    return _app_instance