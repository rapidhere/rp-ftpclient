import ftpparse


def parse_line(buf):
    if buf[-1] == '\n':
        buf = buf[:-1]
    ret_tuple = ftpparse.ftp_list_parse(buf)
    if not ret_tuple:
        # Parse Failed
        return None

    # Find out the type of the file
    flag_cwd = bool(ret_tuple[1])
    flag_retr = bool(ret_tuple[2])
    t = ''
    if flag_cwd and flag_retr:
        t = 'l'
    elif flag_cwd and not flag_retr:
        t = 'd'
    elif not flag_cwd and flag_retr:
        t = 'f'

    time = ret_tuple[6]

    return {
        "name" : ret_tuple[0],
        "type" : t,
        "size" : ret_tuple[4],
        "time" : time,
        "id"   : ret_tuple[-1]
    }