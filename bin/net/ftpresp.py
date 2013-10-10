#!/usr/bin/python
#-*- coding:utf-8 -*-


class FTPResponse:
    def __init__(self, resp_code=0, resp_text=""):
        self.set_resp_code(resp_code)
        self.set_resp_text(resp_text)

    def set_resp_code(self, resp_code):
        self.resp_code = int(resp_code)

    def set_resp_text(self, resp_text):
        self.resp_text = resp_text

    def get_resp_code(self):
        return self.resp_code

    def get_resp_text(self):
        return self.resp_text

    def __repr__(self):
        return "%d %s" % (self.get_resp_code(), self.get_resp_text())

    def get_pair(self):
        return self.get_resp_code(), self.get_resp_text()