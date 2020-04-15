# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/4/7 20:44
file  :test_invest.py
===============================
"""
import unittest
import os
import jsonpath
from common.handler_logging import log
from requests import request
from library.myddt import ddt, data
from common.handler_doexcel import DoExcle
from common.handler_path import DATA_DIR
from common.handler_config import conf
from common.handler_data import EnvData, replace_data

filename = os.path.join(DATA_DIR, 'cases_code.xlsx')


@unittest.skip
@ddt
class InvestTestCase(unittest.TestCase):
    excel = DoExcle(filename, 'invest')
    case_data = excel.read_excle_data_is_dict_02()

    @data(*case_data)
    def test_invest(self, case):
        '''投资用例'''
        # 第一步：准备数据
        url = conf.get('env', 'service') + case['url']
        method = case['method']
        headers = eval(conf.get('env', 'headers'))
        if case['interface'] != 'login':
            # 如果不是登录接口，则添加个token
            headers['Authorization'] = getattr(EnvData,'token')
        data = eval(replace_data(case['data']))
        expected = case['expected']
        # 第二步：发送请求，获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        if case['interface'] == 'login':
            # 如果是登录接口则提取用户id和token
            member_id = str(jsonpath.jsonpath(res, '$..id')[0])
            token = 'Bearer' + ' ' + str(jsonpath.jsonpath(res, '$..token')[0])
            setattr(EnvData, 'member_id', member_id)
            setattr(EnvData, 'token', token)
        if case['interface'] == 'add':
            # 如果是加标接口则提取标id进行保存
            loan_id = str(jsonpath.jsonpath(res,'$..id')[0])
            setattr(EnvData,'loan_id',loan_id)
        # 第三步：断言
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            result = 'PASS'
            log.info('用例：{}，执行结果:{}\n'.format(case['title'], result))
        except AssertionError as e:
            # 异常处理
            result = 'Fail'
            log.error('用例：{}，执行结果:{}，错误信息{}'.format(case['title'], result, e))
            log.debug('预期结果：{}'.format(expected))
            log.debug('实际结果：{}'.format(res))
            log.exception('{}\n'.format(e))
            raise e
        finally:
            self.excel.back_write(case['case_id'] + 1, 8, str(res))
            self.excel.back_write(case['case_id'] + 1, 9, result)



'''
投资接口的前置条件：
1.有可以投资的项目：
    创建一个项目（普通用户登录：借款人）：2个请求
    审核通过（管理员登录）2个请求

2.用户要有钱
    -投资人（普通用户）登录：1个请求
    -投资人充值：一个请求
    
3.执行投资相关的用例

'''
