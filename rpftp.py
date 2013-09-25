#!/usr/bin/python
#-*- coding:utf-8 -*-

# The entry of the app

from bin import rfapp

if __name__ == "__main__":
    app = rfapp.get_app()
    app.run()