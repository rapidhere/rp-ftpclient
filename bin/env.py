# !/usr/bin/python
# -*- coding:utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk

# Window Settings
DEFAULT_WIN_SIZE = (800, 500)
WIN_TITLE = "rp-ftp-client"

# Menu bar Settings
# MENU_BAR_CONFIG = {}
# This item describe the structure of the menu bar
# Now it's in bin.rfapp._load_up_menubar

# File View Settings
FILE_VIEW_HEIGHT = 300
FILE_VIEW_WIDTH = 500

# Resp bar Settings :
RESP_VIEW_WELCOME_INFO = "Welcome to use rp-ftp-client ..."
RESP_VIEW_BACKGROUND_COLOR = "#F0F8FF"
RESP_VIEW_FONT = "Monospace 12"

RESP_VIEW_INFO_FONT_COLOR = "#1010FF"
RESP_VIEW_WARNING_FONT_COLOR = "#10FFFF"
RESP_VIEW_ERROR_FONT_COLOR = "#FF1010"
RESP_VIEW_SEND_CMD_FONT_COLOR = "#10FF10"
RESP_VIEW_SERVER_RESP_FONT_COLOR = "#FF10FF"

RESP_VIEW_MAX_LINE = 100