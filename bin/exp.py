class RFFTPException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


# { FTP Exceptions
class FTPException(RFFTPException):
    def __init__(self, ex_info):
        RFFTPException.__init__(self, "ftp connection error: %s" % ex_info)


class FTPConnectFailed(FTPException):
    def __init__(self, host, port):
        FTPException.__init__(self, "Connect to host <%s:%d> failed!" % (host, port))


class FTPMakePortFailed(FTPException):
    def __init__(self):
        FTPException.__init__(self, "Failed to find a usable port for PORT command")


class FTPRuntimeException(FTPException):
    def __init__(self, resp):
        resp_id = resp.get_resp_code()
        resp_text = resp.get_resp_text()

        FTPException.__init__(self, "[%d %s]" % (resp_id, resp_text))


class FTPTemporaryError(FTPRuntimeException):
    pass


class FTPPermanentError(FTPRuntimeException):
    pass
# }