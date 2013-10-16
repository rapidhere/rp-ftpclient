#!/usr/bin/python
#-*- coding:utf-8 -*-

from bin import exp, env


class CMDParser:
    def __init__(self):
        self._cmd_list = {}

        for cmd_tuple in env.CMD_LIST:
            self.register_cmd(cmd_tuple[0], cmd_tuple[1])

    def _get_filter(self, filt_name):
        return getattr(self, "_filter_" + filt_name)

    def register_cmd(self, cmd_name, par_tuple):
        ret = []
        for par in par_tuple:
            par = par.split(":")
            cret = (par[0], [])
            for filt in par[1:]:
                cret[1].append(self._get_filter(filt))
            ret.append(cret)

        self._cmd_list[cmd_name] = ret

    def parse_cmd_line(self, cmd_line):
        par_dict = {}

        args = []
        for x in cmd_line.split(" "):
            if x:
                args.append(x)

        cmd_name = args[0]
        if not cmd_name in self._cmd_list:
            raise exp.CMDNotFound(cmd_name)
        args = args[1:]

        index = 0
        for par in self._cmd_list[cmd_name]:
            par_val = ''
            if index < len(args):
                par_val = args[index]

            for filt in par[1]:
                par_val = filt(par_val, cmd_name, index, par[0])

            par_dict[par[0]] = par_val

            index += 1

        return cmd_name, par_dict

    def _filter_require(self, arg, *args):
        if not arg:
            raise exp.CMDRequiredArgument(*args)
        return arg

    def _filter_int(self, arg, *args):
        if not arg:
            return arg

        try:
            return int(arg)
        except ValueError:
            raise exp.CMDIntegerArgument(*args)

    def _filter_none(self, arg, *args):
        return arg

_cmd_parser_instance = None


def get_cmd_parser():
    global _cmd_parser_instance
    if not _cmd_parser_instance:
        _cmd_parser_instance = CMDParser()

    return _cmd_parser_instance