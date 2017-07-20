#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

class mysql:
    def __init__(self):
        print 1;

    def connect(self):
        # 打开数据库连接
        db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )