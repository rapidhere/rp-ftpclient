#!/usr/bin/python
#-*- coding :utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk
import gobject

from bin.ui import get_window, MenuBar, get_file_view, get_response_view, get_directory_view, get_console_view
from bin.ui.dialogs import BaseConnectDialog, BASE_CONNECT_DIA_BT_CONNECT, BASE_CONNECT_DIA_BT_CANCEL
from bin import env
from bin.net import get_ftp, FTPResponse
from bin.widget import FileNode, get_directory_tree, filenode_new_from_line, \
    FILE_TYPE_DIR
import exp


class RFApp(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)
        self.ftp = get_ftp()

        self.win = get_window()
        self._load_up_menubar()
        self._load_up_file_view()
        self._load_up_directory_view()
        self._load_up_console_view()
        self._load_up_resp_bar()

        self._set_up_layout()

        self.dir_tree = get_directory_tree()

        # Connect signals
        self.win.connect("destroy", lambda w: self.exit())
        self.ftp.connect("rf-ftp-response", self._on_ftp_response)
        self.ftp.connect("rf-ftp-send-cmd", self._on_ftp_send_cmd)

        self.win.show()

    def run(self):
        gtk.main()

    def _set_up_layout(self):
        # Set up layout
        vbox = gtk.VBox(False)
        vbox.pack_start(self.menubar, False, False)

        # { Global Pane
        paned = gtk.VPaned()
        ## { Pane on the top
        paned1 = gtk.HPaned()
        paned1.add1(self.file_view)
        paned1.add2(self.directory_view)
        paned1.show()
        paned.add1(paned1)
        ## } { Page on the bottom
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.append_page(self.resp_bar, gtk.Label("Response"))
        notebook.append_page(self.console_view, gtk.Label("Console"))
        notebook.show_all()
        paned.add2(notebook)
        paned.show()
        ## }
        vbox.pack_start(paned, True, True)
        # }

        vbox.show()
        self.win.add(vbox)

    def _load_up_menubar(self):
        MENU_BAR_CONF = (
            (
                "_connect",
                ["_simple connect", self._on_menubar_base_connect],
                ["_advanced connect", self._on_menubar_advanced_connect],
                None,
                ["_history", self._on_menubar_history],
                None,
                ["_disconnect", self._on_menubar_disconnect]
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

    def _load_up_directory_view(self):
        self.directory_view = get_directory_view()

    def _load_up_file_view(self):
        self.file_view = get_file_view()

    def _load_up_resp_bar(self):
        self.resp_bar = get_response_view()
        self.resp_bar.append_info_line(env.RESP_VIEW_WELCOME_INFO)

    def _load_up_console_view(self):
        self.console_view = get_console_view()

    def _new_connection(self, host, usr, psw,
                        port=None,
                        acct=None,
                        data_type=None,
                        data_structure=None,
                        trans_mode=None,
                        connect_mode=None):
        if port:
            self.ftp.connect_to_host(host, port)
        else:
            self.ftp.connect_to_host(host)

        if data_type:
            self.resp_bar.append_info_line("Configuring data type ...")
            self.ftp.set_data_type(data_type)

        if data_structure:
            self.resp_bar.append_info_line("Configuring data structure ..")
            self.ftp.set_data_structure(data_structure)

        if trans_mode:
            self.resp_bar.append_info_line("Configuring transmit mode ...")
            self.ftp.set_data_transmission_mode(trans_mode)

        if connect_mode:
            self.resp_bar.append_info_line("Configuring connect mode ...")
            self.ftp.set_transfer_mode(connect_mode)

        self.ftp.login(usr, psw, acct)

        root_dir = self.ftp.print_current_dir()
        root_fn = FileNode(name=root_dir, type=FILE_TYPE_DIR)
        self.dir_tree.set_root(root_fn)

    def _on_menubar_base_connect(self, widget, data=None):
        dia = BaseConnectDialog(self.win)
        resp = dia.run()

        if resp.resp_id == BASE_CONNECT_DIA_BT_CONNECT:
            try:
                self._new_connection(resp.hst, resp.usr, resp.pss, resp.prt)
            except (exp.FTPConnectFailed, exp.FTPMakePortFailed) as e:
                self.resp_bar.append_error_line(str(e))
                self.ftp.close()
        elif resp.resp_id == BASE_CONNECT_DIA_BT_CANCEL:
            pass

    def _on_ftp_response(self, widget, resp_id, resp_text):
        resp = FTPResponse(resp_id, resp_text)
        c = resp.get_resp_code() / 100
        if c == 4:
            self.resp_bar.append_server_resp_warning(resp)
        elif c == 5:
            self.resp_bar.append_server_resp_error(resp)
        else:
            self.resp_bar.append_server_resp_info(resp)

    def _on_ftp_send_cmd(self, widget, cmd):
        self.resp_bar.append_send_cmd_info(cmd)

    def _on_menubar_advanced_connect(self, widget, data=None):
        pass

    def _on_menubar_history(self, widget, data=None):
        pass

    def _on_menubar_disconnect(self, widget, data=None):
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