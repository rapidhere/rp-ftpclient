#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from inputdia import InputDialog

BASE_CONNECT_DIA_BT_CONNECT = 1
BASE_CONNECT_DIA_BT_CANCEL = 2


DIALOG_CONFIG = (
    ("Host", "hst", True),
    ("Username", "usr", True),
    ("Password", "pss", False)
)


class BaseConnectDialog(InputDialog):
    def __init__(self, parent):
        InputDialog.__init__(self, parent)

        # Build up ui
        self.tbl_box = gtk.Table(len(DIALOG_CONFIG), 2)
        self.tbl_box.set_col_spacings(5)
        self.tbl_box.set_row_spacings(5)

        for it in DIALOG_CONFIG:
            self._add_entry(it[0], it[1], it[2], DIALOG_CONFIG.index(it))

        self.vbox.pack_start(self.tbl_box)
        self.tbl_box.show_all()

        self.add_button("C_onnect", BASE_CONNECT_DIA_BT_CONNECT)
        self.add_button("_Cancel", BASE_CONNECT_DIA_BT_CANCEL)

    def _add_entry(self, label, entry_name, visibility, column):
        lab = gtk.Label(label)
        lab.set_justify(gtk.JUSTIFY_RIGHT)
        self.tbl_box.attach(lab, 0, 1, column, column + 1)

        entry = gtk.Entry(80)
        entry.set_visibility(visibility)
        self.tbl_box.attach(entry, 1, 2, column, column + 1)

        setattr(self, entry_name + "_entry", entry)

    def retrieve_data(self):
        ret = {}
        for it in DIALOG_CONFIG:
            ent_name = it[1]
            entry = getattr(self, ent_name + "_entry")
            ret[ent_name] = entry.get_text()
        return ret