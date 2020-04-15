# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/24 21:45
file  :handler_path.py
===============================
"""
import os


# 获取项目所在的绝对路径
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 用例模块所在的路径
CASE_DIR = os.path.join(BASE_DIR,'testcase')

# 用例数据所在的路径
DATA_DIR = os.path.join(BASE_DIR,'case_data')

# 配置文件所在的路径
CONF_DIR = os.path.join(BASE_DIR,'conf')

# 测试报告所在的路径
REPORT_DIR = os.path.join(BASE_DIR,'report')

# 日志文件所在的路径
LOG_DIR = os.path.join(BASE_DIR,'logs')