#!/usr/bin/python
#-*- coding:utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk

from bin.widget import FileNode


def filenode_new_from_line(str_line):
    fn = FileNode()
    buf = []
    for item in str_line.split(" "):
        if item:
            buf.append(item)

    fn.set_mode(buf[0])
    fn.set_nind(buf[1])
    fn.set_owner(buf[2])
    fn.set_group(buf[3])
    fn.set_size(buf[4])
    fn.set_size(buf[5] + buf[6])
    fn.set_time(buf[7])
    fn.set_name(buf[8])

    return fn