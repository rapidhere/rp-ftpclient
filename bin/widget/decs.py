#!/usr/bin/python
#-*- coding:utf-8 -*-

from utils import tree_dir_path_to_string


def std_path_notify_function(emit_signal):
        def _dec_func(func):
            def _func(self, *args, **kwargs):
                node = kwargs.get("node", None)
                if not node:
                    path = kwargs.get("path", None)
                    if path:
                        node = self.get_node(path)
                    else:
                        node = self.cur_node

                if "node" in kwargs:
                    del kwargs["node"]

                if "path" in kwargs:
                    del kwargs["path"]

                ret_node = func(self, node, *args, **kwargs)

                self.emit(emit_signal, tree_dir_path_to_string(ret_node.get_path_tuple()))

            return _func
        return _dec_func