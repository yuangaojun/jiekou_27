# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/18 22:17
file  :handler_logging.py
===============================
"""
# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/18 21:39
file  :handler_logging.py
===============================
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from common.handler_config import conf
from common.handler_path import LOG_DIR


class HnadlerLogging():
    '''收集日志封装类'''

    def create_log(self):
        # 创建日志收集器对象
        log = logging.getLogger('yuan')
        # 设置日志收集等级
        log.setLevel(conf.get('log', 'log_level'))
        # 日志保存路径
        log_dir = LOG_DIR
        # 创建日志收集器输出渠道
        fh_log = TimedRotatingFileHandler(filename=os.path.join(log_dir,conf.get('log', 'filename')),
                                          encoding='utf-8',
                                          when='S',
                                          interval=60,
                                          backupCount=3)
        # 设置日志输出等级
        fh_log.setLevel(conf.get('log', 'fh_level'))
        log.addHandler(fh_log)
        # 设置日志输出格式
        formats = conf.get('log', 'format')
        format = logging.Formatter(formats)
        fh_log.setFormatter(format)
        # 接收日志
        return log


log = HnadlerLogging().create_log()
