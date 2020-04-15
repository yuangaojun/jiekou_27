# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/18 22:17
file  :handler_config.py
===============================
"""
import os
# from configparser import ConfigParser
from configparser import RawConfigParser
from common.handler_path import CONF_DIR


def create_config_path():
    '''读取配置文件路径'''
    config_path = os.path.join(CONF_DIR, 'lemon01.ini')
    return config_path


class HandlerConfig(RawConfigParser):
    '''配置文件解释器类'''

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding='utf-8')


conf = HandlerConfig(create_config_path())
