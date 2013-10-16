#!/usr/bin/python
#-*- coding:utf-8 -*-


from bin.widget.filenode import FileNode, FILE_TYPE_FILE, FILE_TYPE_LINK, FILE_TYPE_DIR
from bin.net.ftpparse import parse_line
import datetime


def dir_tuple_to_path(t):
    return "/".join(t)


def tree_dir_path_to_string(path_tuple):
    return "\n".join([repr(x) for x in path_tuple])


def tree_dir_string_to_path(string):
    return tuple([int(x) for x in string.split("\n")])


def filenode_new_from_line(str_line):
    fn = FileNode()
    ret = parse_line(str_line)
    fn.set_name(ret["name"])
    fn.set_size(ret["size"])

    time = ret["time"]
    if not time:
        fn.set_date(None)
        fn.set_time(None)
    else:
        dt = datetime.datetime.fromtimestamp(int(time))
        fn.set_date(dt.date().isoformat())
        fn.set_time(dt.time().isoformat())

    if ret["type"] == 'l':
        fn.set_type(FILE_TYPE_LINK)
    elif ret["type"] == 'f':
        fn.set_type(FILE_TYPE_FILE)
    elif ret["type"] == 'd':
        fn.set_type(FILE_TYPE_DIR)

    return fn