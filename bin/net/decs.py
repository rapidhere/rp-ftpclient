#!/usr/bin/python
#-*- coding:utf-8 -*-
from constants import *


def _require_data_connection_function(func):
        def _func(self, *args, **kwargs):
            md = self.get_transfer_mode()
            if md == FTP_CONNECT_MODE_PASSIVE:
                self.make_pasv()
            elif md == FTP_CONNECT_MODE_POSITIVE:
                self.make_port()
            ret = func(self, *args, **kwargs)
            self._data_conn.close()
            self._data_file.close()
            return ret

        return _func


def _response_function(func):
    def _func(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self._process_response()

    return _func