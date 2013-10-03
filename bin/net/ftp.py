#!/usr/bin/python
#-*- coding:utf-8 -*-

from ftpresp import FTPResponse
from bin import exp, env
import re

import pygtk
pygtk.require("2.0")
import gobject
import socket
from ftplib import CRLF

# Constants
FTP_DATA_TYPE_ASCII = 'A'
#FTP_DATA_TYPE_EBCDIC = 'E'
FTP_DATA_TYPE_IMAGE = 'I'
#FTP_DATA_TYPE_LOCAL = 'L'

FTP_DATA_STRUCTURE_FILE = 'F'
#FTP_DATA_STRUCTURE_RECORD = 'R'
#FTP_DATA_STRUCTURE_PAGE = 'P'

FTP_DATA_TRANSMISSION_MODE_STREAM = 'S'
FTP_DATA_TRANSMISSION_MODE_BLOCK = 'B'
FTP_DATA_TRANSMISSION_MODE_COMPRESSED = 'C'

FTP_CONNECT_MODE_PASSIVE = "PASS"
FTP_CONNECT_MODE_POSITIVE = "PORT"

# Default:
FTP_DEFAULT_CONNECT_MODE = FTP_CONNECT_MODE_PASSIVE
FTP_DEFAULT_CONNECT_TIMEOUT = 60


class FTP(gobject.GObject):
    # Decorators: {
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
    # }

    def __init__(self):
        gobject.GObject.__init__(self)
        self._data_conn = None
        self._sock = self._sock_file = None
        self.set_transfer_mode(FTP_DEFAULT_CONNECT_MODE)

    @_response_function
    def connect(self, host, port=21, timeout=FTP_DEFAULT_CONNECT_TIMEOUT):
        # Connect to specified host, port
        self._sock = socket.create_connection((host, port), timeout)
        self._sock_file = self._sock.makefile("rb")

    @_response_function
    def send_cmd(self, cmd, cmd_pars=None):
        if cmd_pars:
            if type(cmd_pars) == str:
                cmd += " " + cmd_pars
            else:
                for par in cmd_pars:
                    cmd += " " + par
        buf = cmd + CRLF
        self._sock.sendall(buf)

    def set_data_type(self, type=FTP_DATA_TYPE_ASCII):
        self.send_cmd("TYPE", type)

    def set_data_structure(self, structure=FTP_DATA_STRUCTURE_FILE):
        self.send_cmd("STRU", structure)

    def set_data_transmission_mode(self, mode=FTP_DATA_TRANSMISSION_MODE_STREAM):
        self.send_cmd("MODE", mode)

    def login(self, username='anonymous', password='', account=''):
        resp = self.send_cmd("USER", username)

        if resp.get_resp_code() == 331:
            resp = self.send_cmd("PASS", password)
        if resp.get_resp_code() == 332:
            resp = self.send_cmd("ACCT", account)
        if resp.get_resp_code() == 230:
            raise exp.FTPRuntimeException(resp)

    def set_transfer_mode(self, md):
        self._transfer_mode = md

    def get_transfer_mode(self):
        return self._transfer_mode

    def make_pasv(self, timeout=FTP_DEFAULT_CONNECT_TIMEOUT):
        resp = self.send_cmd("PASV")
        pat = re.compile(
            r"""
            \(                          # Start
            (?P<host>\d+,\d+,\d+,\d+),  # Host
            (?P<port1>\d+),             # Port high 8bit
            (?P<port2>\d+)              # Port low 8bit
            \)                          # End
            """, re.VERBOSE)
        mat = pat.search(resp.get_resp_text()).groupdict()
        host = mat["host"].replace(',', '.')
        port = str((int(mat["port1"]) << 8) + int(mat["port2"]))

        self._data_conn = socket.create_connection((host, port), timeout)
        self._data_file = self._data_conn.makefile("rb")
        return host, port

    def make_port(self, timeout=FTP_DEFAULT_CONNECT_TIMEOUT):
        # Find a empty port
        sock = None
        for ret in socket.getaddrinfo(None, 0, self._sock.family, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, st, pr, ca, sa = ret
            try:
                sock = socket.socket(af, st, pr)
                sock.bind(sa)
            except socket.error as msg:
                if sock:
                    sock.close()
                sock = None
                continue

        if not sock:
            raise exp.FTPMakePortFailed

        sock.listen(5)
        port = sock.getsockname()[1]
        host = self._sock.getsockname()[0]
        self.send_cmd("PORT", ",".join(host.split(".") + [str(port // 256), str(port % 256)]))
        sock.settimeout(timeout)

        self._data_conn = sock
        self._data_file = sock.makefile("rb")
        return host, port

    @_require_data_connection_function
    def list_current_dir(self):
        self.send_cmd("LIST")
        buf = self._get_all_line(self._data_file)
        self._process_response()
        return buf

    def print_current_dir(self):
        resp = self.send_cmd("PWD")
        return resp.get_resp_text()[1:-1]

    def change_dir(self, path_name):
        self.send_cmd("CWD", path_name)

    def close(self):
        if self._sock:
            self._sock.close()
        if self._sock_file:
            self._sock_file.close()

        self._sock = self._sock_file = None

    def quit(self):
        resp = self.send_cmd("QUIT")
        self.close()

    def _get_line(self, _file):
        buf = _file.readline()

        if buf[-2:] == CRLF:
            buf = buf[:-2]
        elif buf[-1:] in CRLF:
            buf = buf[:-1]

        return buf

    def _get_all_line(self, _file):
        buf = ""

        while True:
            buff = self._get_line(_file)
            if not buff:
                break
            buf += buff + "\n"
        return buf

    def _process_multiple_line(self, _file):
        buf = self._get_line(_file)
        if buf[3] == '-':
            # A multiple line response
            resp_code = buf[:-3]
            while True:
                cbuff = self._get_line(_file)
                buf = (buf + "\n" + cbuff)

                if cbuff[:3] == resp_code and cbuff[3] != '-':
                    break
        return buf

    def _process_response(self):
        buf = self._process_multiple_line(self._sock_file)
        resp_code = int(buf[:3])
        resp_text = buf[4:]
        resp = FTPResponse(resp_code, resp_text)
        try:
            c = resp_code / 100
            if c == 4:
                raise exp.FTPTemporaryError(resp)
            elif c == 5:
                raise exp.FTPPermanentError(resp)
            else:
                # c in (1, 2, 3)
                # omitted
                pass
        finally:
            pass
            #self.emit("rf-ftp-response", (resp_code, resp_text))

        return resp

SIGNAL_FTP_RESPONSE = gobject.signal_new(
    "rf-ftp-response",
    FTP, gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_BOOLEAN,
    (gobject.TYPE_INT, gobject.TYPE_STRING)
)