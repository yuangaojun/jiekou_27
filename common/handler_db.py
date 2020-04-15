# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/26 20:39
file  :03操作数据库模块的封装.py
===============================
"""
'''
封装的需求：
    1.查询数据的方法
    2.增删改的方法
    3.__init__方：法建立连接

'''
import pymysql
from common.handler_config import conf

class HandlerMysql():

    def __init__(self):
        '''初始化方法中连接到数据库'''
        # 第一步连接到数据库
        self.con = pymysql.connect(host=conf.get('mysql','host'),
                               port=conf.getint('mysql','port'),
                               user=conf.get('mysql','user'),
                               password=conf.get('mysql','password'),
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def find_all(self,sql):
        '''
        查询sql语句返回的所有数据
        :param sql: 查询的sql
        :return:查询到的所有数据
        '''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one(self,sql):
        '''
        查询sql语句返回的第一条数据
        :param sql:查询的sql
        :type sql:str
        :return:sql语句查询到的第一条数据
        '''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_count(self,sql):
        '''
        查询sql语句查询到的条输
        :param sql: 查询的sql
        :return:查询到的条数
        '''
        self.con.commit()
        res = self.cur.execute(sql)
        return res


    def update(self,sql):
        '''
        增删改的操作方法
        :param sql: 增删改的sql语句
        :return:
        '''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.commit()

    def close(self):
        '''断开游标，关闭连接'''
        self.cur.close()
        self.con.close()


