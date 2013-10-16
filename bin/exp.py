class RFFTPException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


# { FTP Exceptions
class FTPException(RFFTPException):
    def __init__(self, ex_info):
        RFFTPException.__init__(self, "ftp connection error: %s" % ex_info)


class FTPConnectFailed(FTPException):
    def __init__(self, host, port, info):
        FTPException.__init__(self, "Connect to host <%s:%d> failed: %s" % (host, int(port), info))


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


# { CMD Exceptions
class CMDException(RFFTPException):
    pass


class CMDNotFound(CMDException):
    def __init__(self, cmd_name):
        CMDException.__init__(self, "%s is not a valid command!" % cmd_name)


class CMDArgumentError(CMDException):
    def __init__(self, cmd_name, index, cmd_argu, ex_info):
        CMDException.__init__(self, "%s: argument %d[%s]: %s" % (cmd_name, index, cmd_argu, ex_info))


class CMDRequiredArgument(CMDArgumentError):
    def __init__(self, cmd_name, index, cmd_argu):
        CMDArgumentError.__init__(self, cmd_name, index, cmd_argu, "Required Argument Cannot Be Null!")


class CMDIntegerArgument(CMDArgumentError):
    def __init__(self, cmd_name, index, cmd_argu):
        CMDArgumentError.__init__(self, cmd_name, index, cmd_argu, "Argument isn't an integer!")
# }


# { Model- Directory Tree
class DirectoryTreeException(RFFTPException):
    pass


class DirectoryTreeChangeIntoParentFailed(DirectoryTreeException):
    def __init__(self):
        DirectoryTreeException.__init__(self, "This is already the root dir!")


class DirectoryTreeChangeIntoChildFailed(DirectoryTreeException):
    def __init__(self, ch):
        DirectoryTreeException.__init__(self, "%s doesn't exist or is not a directory" % ch)
# }