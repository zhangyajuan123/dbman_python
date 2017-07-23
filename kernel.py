#!/usr/bin/python
# -*- coding: UTF-8 -*-
import utils.mysql as mysql
import utils.utils as utils


class kernel:

    conf = {}
    def __init__(self):
        self.conf = utils.getConfigList('misc')
        self.m = mysql.mysql()

    def __del__(self):
        print '------------- END -------------'


    def update(self):
        database_path = self.conf['data']
        dbFiles = utils.getFileList(database_path)
        for table_name in dbFiles:
            full_file_path = database_path + dbFiles[table_name]
            full_file_content = utils.file2dict(full_file_path)
            # 判断表是否存在
            if self.m.table_exists(table_name):
                # 更新表
                print self.m.getTablesInfo(table_name)
                print '--------- 更新表 ---------'+table_name
            else:
                print '--------- 添加表 ---------'+table_name


