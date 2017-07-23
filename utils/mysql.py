#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

import utils


class mysql:

    conf = {}

    def __init__(self):
        mysql.conf = utils.getConfigList('mysql')
        self.connect()

    def __del__(self):
        if mysql.db :
            mysql.db.close()

    def connect(self):
        # 打开数据库连接
        mysql.db = MySQLdb.connect(mysql.conf['host'],mysql.conf['user'],mysql.conf['pass'],mysql.conf['database'])

    """
    测试方法，获取版本
    """
    def get_version(self):
        # 使用cursor()方法获取操作游标
        cursor = mysql.db.cursor()
        # 使用execute方法执行SQL语句
        cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取一条数据库。
        data = cursor.fetchone()
        # 返回数据
        return data

    """
    查询方法，用于获取原始结果
    """
    def select(self,sql):
        # 使用cursor()方法获取操作游标
        cursor = mysql.db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # 返回结果
            return results
        except:
            print "Error: The query data is fatal!"

    """
    执行方法，用于执行update,delete,drop等语句
    注：此方法是事务性操作，请放心使用
    """
    def execute(self,sql):
        # 使用cursor()方法获取操作游标
        cursor = mysql.db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 向数据库提交
            mysql.db.commit()
            return True
        except:
            # 发生错误时回滚
            mysql.db.rollback()
            return False
        return False

    """
    查询多行方法，因为需要表头，所以没用select、execute方法
    注：这里已经处理过，返回值是一个List
    """
    def getList(self,sql):
        # 使用cursor()方法获取操作游标
        cursor = mysql.db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 表头
            title = cursor.description
            # 获取所有记录列表
            results = cursor.fetchall()
            # 定义返回值
            list = []
            for row in results:
                # 定义一行
                ir = {}
                # 取出所有表头
                for i in range(len(title) - 1):
                    ir[title[i][0]] = row[i]
                # 追加到list里面
                list.append(ir)
            # 返回结果
            return list
        except:
            print "Error: The query data is fatal."

    """
    查询一行的方法，内部调用getList
    """
    def getRow(self,sql):
        # 调用本类getList方法
        data = self.getList(sql)
        if data:
            return data[0]
        return {}

    # 判断表是否存在
    def table_exists(self,table_name):
        database = mysql.conf['database'];
        sql = "select TABLE_NAME AS tablename from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='"+database+"' and TABLE_NAME='"+table_name+"'"
        if self.select(sql):
            return True
        return False

    # 删除表
    def drop_table(self,table_name):
        sql = "DROP TABLE IF EXISTS "+table_name
        return self.execute(sql)

    def getTablesInfo(self,table_name):
        sql = 'SHOW FULL COLUMNS FROM `' + table_name + '`;'
        result = self.getList(sql)
        info = {}
        for row in result:
            #row = row.lower()
            tmp = {
                'type':row['Type'],
                'notnull':row['Null'] == 'NO' if True else False,
                'default':row['Default'] == None and None or row['Default']
            }
            info[row['Field']] = tmp

        return info