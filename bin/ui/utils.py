#!/usr/bin/python
#-*- coding:utf-8 -*-
from bin.widget import get_directory_tree, FILE_TYPE_DIR


def index_dir_child(iter):
    par = iter.get_parent()
    index = 0
    for ch in par.get_child_list():
        fn = ch.get_filenode()
        if fn.get_type() != FILE_TYPE_DIR:
            continue

        if fn.get_name() == iter.get_filenode().get_name():
            return index
        index += 1
    return None


def get_nth_dir_child(iter, index):
    ind = 0
    for ch in iter.get_child_list():
        fn = ch.get_filenode()
        if fn.get_type() != FILE_TYPE_DIR:
            continue

        if ind == index:
            return ch

        ind += 1

    raise IndexError


def dir_path_to_common_path(dp):
    iter = get_directory_tree()._root
    cp = []
    for ind in dp:
        ch = get_nth_dir_child(iter, ind)
        c_ind = iter.index_child(ch)
        cp.append(c_ind)

        iter = ch

    return tuple(cp)


def common_path_to_dir_path(cp):
    iter = get_directory_tree()._root
    dp = []
    for ind in cp:
        ch = iter.get_nth_child(ind)
        d_ind = index_dir_child(ch)
        dp.append(d_ind)

        iter = ch

    return tuple(dp)