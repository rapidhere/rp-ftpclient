#!/usr/bin/python
#-*- coding:utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk

FILE_NODE_ATTR_LIST = ("type", "name", "size", "date", "time")

FILE_TYPE_LINK = 0
FILE_TYPE_FILE = 1
FILE_TYPE_DIR = 2


class FileNode:
    def __init__(self, type="", size=0, date="", time="", name=""):
        self.set_type(type)
        self.set_size(size)
        self.set_date(date)
        self.set_time(time)
        self.set_name(name)

    def set_type(self, t):
        self.type = t

    def get_type(self):
        return self.type

    def set_size(self, s):
        self.size = int(s)

    def get_size(self):
        return self.size

    def set_date(self, d):
        self.date = d

    def get_date(self):
        return self.date

    def set_time(self, t):
        self.time = t

    def get_time(self):
        return self.time

    def set_name(self, n):
        self.name = n

    def get_name(self):
        return self.name

    def to_list(self):
        stock = None
        if self.get_type() == FILE_TYPE_DIR:
            stock = gtk.STOCK_DIRECTORY
        elif self.get_type() == FILE_TYPE_FILE:
            stock = gtk.STOCK_FILE
        elif self.get_type() == FILE_TYPE_LINK:
            stock = gtk.STOCK_DND

        return [stock, self.get_name(), str(self.get_size()), self.get_date(), self.get_time()]