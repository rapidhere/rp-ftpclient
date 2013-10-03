# !/usr/bin/python
# -*- coding:utf-8 -*-


# Window Settings
DEFAULT_WIN_SIZE = (800, 500)
WIN_TITLE = "rp-ftp-client"

# Menu bar Settings
# MENU_BAR_CONFIG = {}
# This item describe the structure of the menu bar
# Now it's in bin.rfapp._load_up_menubar

# File View Settings
FILE_VIEW_HEIGHT = 300

FILE_VIEW_COLUMN_CONFIG = (
    ("mode", 100),
    ("inodes/subdirs", 100),
    ("owner", 50),
    ("group", 50),
    ("size", 50),
    ("date", 100),
    ("time", 100),
    ("name", 100),
)
FILE_VIEW_COLUMN_TYPE_CONFIG = (str, str, str, str, str, str, str, str)

# Resp bar Settings :
RESP_BAR_WELCOME_INFO = "Welcome to use rp-ftp-client ..."
RESP_BAR_BACKGROUND_COLOR = "#F0F8FF"
RESP_BAR_FONT = "Monospace 12"
RESP_BAR_FONT_COLOR = "#220FFF"