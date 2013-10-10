from ftpresp import FTPResponse


def ftp_response_new_from_string(string):
    if not string:
        return FTPResponse(-1, "None")
    return FTPResponse(string[:3], string[4:])