# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/18 22:13
file  :run.py
===============================
"""
import unittest
import time
from BeautifulReport import BeautifulReport
from common.handler_path import CASE_DIR,REPORT_DIR
from common.handler_email import send_eamil


def get_now_time():
    return time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))

def run():
    '''运行函数测试用例'''

    suite = unittest.defaultTestLoader.discover(start_dir=CASE_DIR,
                                                pattern='test*.py',
                                                top_level_dir=None)
    report = BeautifulReport(suite)
    report.report('自动化测试报告',report_dir=REPORT_DIR,filename='report.html')

if __name__ == '__main__':
    run()
    send_eamil()