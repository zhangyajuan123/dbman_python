#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.dom.minidom
import os
import logging
import ConfigParser


##取配置的方法
###参数：k配置的KEY,m配置的模块
def getConfig(k='',m='mysql'):
    config = ConfigParser.ConfigParser()
    config.readfp(open('dbman.ini'))
    if k == '':
        return config.items(m)
    else:
        return config.get(m, k)


##取整个模块的配置
###参数：配置的模块名
def getConfigList(m='mysql'):
    item_list = getConfig('',m)
    config_list = {}
    for c in item_list:
        config_list[c[0]] = c[1]
    return config_list

#Mysql模块的配置
MysqlConf = getConfigList('mysql')
#文件存放目录配置
FilesConf = getConfigList('data_file')

##获取目录下的XML文件列表
###参数：目录路径
def getFileList(dir_path):
    #获取目录XXX列表
    listfile = os.listdir(dir_path)
    #返回结果
    returnlist = {}
    #过滤目录和无用文件
    i = 0
    for f in listfile:
        if os.path.isfile(f):
            #只获取xml文件
            if os.path.splitext(f)[1] == '.xml':
                i += 1
                returnlist[i] = f

    return returnlist




##解析XML文件并放入DB字典
###参数：文件路径
def file2dict(file_path):
    global FilesConf
    #print FilesConf['data']
    #打开xml文档
    dom = xml.dom.minidom.parse('demo.xml')

    #得到文档元素对象
    root = dom.documentElement

    #定义一个数据表描述字典
    database = {'tablename':'','fields':{},'index':{},'v':'','comment':''}

    #遍历文档的每个节点
    for node in root.childNodes:
        if node.nodeType == node.ELEMENT_NODE:

            #得到数据表名称
            if node.nodeName == 'tablename':
                database['tablename'] = node.firstChild.data


            #得到数据表字段
            if node.nodeName == 'fields':
                for n in node.childNodes:
                    if n.nodeName == 'item':
                        #得到字段名称
                        cc = n.getElementsByTagName('fieldsname')
                        c1 = cc[0]
                        #得到字段类型
                        tt = n.getElementsByTagName('fieldstype')
                        t1 = tt[0]
                        tmp = {'name':c1.firstChild.data,'type':t1.firstChild.data}
                        database['fields'][c1.firstChild.data] = tmp
            #得到数据表索引
            if node.nodeName == 'indexs':
                for i in node.childNodes:
                    if i.nodeName == 'item':
                        #得到索引名称
                        ii = i.getElementsByTagName('indexname')
                        i1 = ii[0]
                        #得到索引字段
                        ff = i.getElementsByTagName('indexfields')
                        f1 = ff[0]
                        tmp = {'name':i1.firstChild.data,'fields':f1.firstChild.data}
                        database['index'][i1.firstChild.data] = tmp

            #得到数据表备注
            if node.nodeName == 'comment':
                database['comment'] = node.firstChild.data

    return database


##写日志方法
###参数：要记录的信息
def __debuglog(_info):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',#需修改，这里可以做能配置
                    filemode='a')#"filemode=a"表示追加|"filemode=w"覆盖
    logging.info(_info)







#测试file2dict方法
database = file2dict('xxx')
for k,val in database.items():
    if k == 'fields':
        for k,v in val.items():
            print v['type'],'---',v['name']
    if k == 'tablename':
            print '表名：',val
    if k == 'comment':
            print '备注：',val


#获取当前工作路径
dir_path = os.getcwd()
print dir_path

#测试getFileList方法
filelist = getFileList(dir_path)
print filelist

#测试__debuglog方法
__debuglog('xxxxxxxx')



