# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/4/8 20:20
file  :handler_data.py
===============================
"""
import re
from common.handler_config import conf

class EnvData():
    '''提取数据临时容器'''

    pass

def replace_data(data):
    while re.search('#(.*?)#',data):
        # 返回一个匹配的对象
        res = re.search('#(.*?)#',data)
        # 返回一个匹配到的数据值
        key = res.group()
        # 返回匹配规则中括号中的数据值
        item = res.group(1)
        try:
            # 去配置文件中获取值
            value = conf.get('test_data',item)
        except:
            # 去EnvData类里面去获取类属性
            value = getattr(EnvData,item)
        data = data.replace(key,value)
    return data

# def replace_data(data):
#     while re.search('#(.*?)#',data):
#         # 返回一个匹配对象
#         res = re.search('#(.*?)#',data)
#         # 返回一个匹配规则匹配到的值
#         key = res.group()
#         # 返回一个匹配规则匹配到的括号中的值
#         item = res.group(1)
#         try:
#             value = conf.get('test_data',item)
#         except:
#             value = getattr(EnvData,item)
#         data = data.replace(key,value)
#     return data


