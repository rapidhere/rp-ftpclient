#!/usr/bin/python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk


class InputDialog(gtk.Dialog):
    def __init__(self, parent):
        gtk.Dialog.__init__(self, parent=parent)

        self.connect_after("response", self._on_response)

    def run(self):
        resp_id = gtk.Dialog.run(self)
        resp = InputDialogResponse(resp_id)

        resp.merge_dict(self._resp_buf)

        return resp

    def _on_response(self, widget, data=None):
        self._resp_buf = self.retrieve_data()

        self.destroy()

    # This is a hook function
    def retrieve_data(self):
        return {}


class InputDialogResponse:
    def __init__(self, resp_id):
        self.resp_id = int(resp_id)

    def merge_dict(self, _dict):
        for key in _dict:
            setattr(self, key, _dict[key])