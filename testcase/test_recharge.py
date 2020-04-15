# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/28 9:36
file  :test_recharge.py
===============================
"""
import os
import unittest
import jsonpath
import decimal
from common.handler_logging import log
from requests import request
from library.myddt import ddt, data
from common.handler_doexcel import DoExcle
from common.handler_path import DATA_DIR
from common.handler_config import conf
from common.handler_db import HandlerMysql
from common.handler_data import EnvData,replace_data


@ddt
class TestRecharge(unittest.TestCase,EnvData):
    excel = DoExcle(os.path.join(DATA_DIR, 'cases_code.xlsx'), 'recharge')
    cases = excel.read_excle_data_is_dict_02()
    db = HandlerMysql()

    @classmethod
    def setUpClass(cls):
        '''用例执行的前置条件：登录'''
        # 准备登录的数据
        url = conf.get('env', 'service') + '/member/login'
        data = {
            'mobile_phone': conf.get('test_data', 'phone'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        response = request(method='post', url=url, json=data, headers=headers)
        res = response.json()
        member_id = str(jsonpath.jsonpath(res, '$..id')[0])
        token = 'Bearer' + ' ' + jsonpath.jsonpath(res, '$..token')[0]
        setattr(EnvData,'member_id',member_id)
        setattr(EnvData,'token',token)
        # setattr()

    @data(*cases)
    def test_recharge(self, case):
        '''充值接口测试方法'''

        # 第一步：准备用例数据
        url = conf.get('env', 'service') + case['url']
        method = case['method']
        # 准备用例参数
        # case['data'] = case['data'].replace('#member_id#', self.member_id)
        case['data'] = replace_data(case['data'])
        # 转换为字典
        data = eval(case['data'])
        # 请求头
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.token
        excepted = eval(case['expected'])
        # 判断该用例是否需要数据库校验，获取充值之前的余额
        if case['check_sql']:
            sql = case['check_sql'].format(self.member_id)
            strt_money = self.db.find_one(sql)['leave_amount']

        # 第二步：发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        # 获取充值之后的余额
        if case['check_sql']:
            sql = case['check_sql'].format(self.member_id)
            end_money = self.db.find_one(sql)['leave_amount']

        # 第三步：断言预期结果和实际结果
        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            # 判断是否需要进行sql校验
            if case['check_sql']:
                # 将充值金额转换为decimal类型，因为数据库的金额是decimal类型
                recharge_money = decimal.Decimal(str(data['amount']))
                self.assertEqual(recharge_money, end_money - strt_money)
            result = 'PASS'
            log.info('用例：{}，执行结果:{}\n'.format(case['title'], result))
        except AssertionError as e:
            # 异常处理
            result = 'Fail'
            log.error('用例：{}，执行结果:{}，错误信息{}'.format(case['title'], result, e))
            log.debug('预期结果：{}'.format(excepted))
            log.debug('实际结果：{}'.format(res))
            log.exception('{}\n'.format(e))
            raise e
        finally:
            self.excel.back_write(case['case_id'] + 1, 8, str(res))
            self.excel.back_write(case['case_id'] + 1, 9, result)
