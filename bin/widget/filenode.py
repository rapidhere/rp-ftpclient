#!/usr/bin/python
#-*- coding:utf-8 -*-

FILE_NODE_ATTR_LIST = ("mode", "nind", "owner", "group", "size", "date", "time", "name")

from bin import env


class FileNode:
    def __init__(self, mode="", nind=0, owner=0, group=0, size=0, date="", time="", name=""):
        self.set_mode(mode)
        self.set_nind(nind)
        self.set_owner(owner)
        self.set_group(group)
        self.set_size(size)
        self.set_date(date)
        self.set_time(time)
        self.set_name(name)

    def __getattr__(self, attr):
        if attr[:4] == "set_":
            attr = attr[4:]
            if attr in FILE_NODE_ATTR_LIST:
                ind = FILE_NODE_ATTR_LIST.index(attr)
                t = env.FILE_VIEW_COLUMN_TYPE_CONFIG[ind]
                return lambda x: setattr(self, attr, t(x))
        elif attr[:4] == "get_":
            attr = attr[4:]
            if attr in FILE_NODE_ATTR_LIST:
                return lambda: getattr(self, attr)
        else:
            raise AttributeError("No such attribute" + attr)

    def to_list(self):
        return [getattr(self,x) for x in FILE_NODE_ATTR_LIST]