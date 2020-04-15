# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/31 20:48
file  :test_audit.py
===============================
"""
'''
审核接口
前置条件：
1.管理员登录，
2.有待审核的项目
    每个审核用例执行之前，去添加一个项目（普通用户添加）
    添加项目之前，普通用户也要的登录

'''

import unittest
import os
import jsonpath
from common.handler_doexcel import DoExcle
from common.handler_path import DATA_DIR
from library.myddt import ddt, data
from common.handler_config import conf
from requests import request
from common.handler_logging import log
from common.handler_db import HandlerMysql


@ddt
class TestAudit(unittest.TestCase):
    excel = DoExcle(os.path.join(DATA_DIR, 'cases_code.xlsx'), 'audit')
    cases = excel.read_excle_data_is_dict_02()
    db = HandlerMysql()

    @classmethod
    def setUpClass(cls):
        # 该用例类所有用例执行之前的前置条件：管理员，普通用户登录
        url = conf.get('env', 'service') + '/member/login'
        headers = eval(conf.get('env', 'headers'))
        # 前置条件一：管理员登录
        admin_data = eval(conf.get('env', 'admin_data'))
        admin_response = request(method='post', url=url, json=admin_data, headers=headers)
        admin_res = admin_response.json()
        # 获取管理员token
        cls.admin_token = 'Bearer' + ' ' + jsonpath.jsonpath(admin_res, '$..token')[0]
        # 前置条件二：普通用户登录
        user_data = eval(conf.get('env', 'data'))
        user_rseponse = request(method='post', url=url, json=user_data, headers=headers)
        user_res = user_rseponse.json()
        # 提取普通用户id和token
        cls.user_member_id = jsonpath.jsonpath(user_res, '$..id')[0]
        cls.user_token = 'Bearer' + ' ' + jsonpath.jsonpath(user_res, '$..token')[0]

    def setUp(self):
        # 每条用例之前的前置条件：添加一个新的项目
        url = conf.get('env', 'service') + '/loan/add'
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.user_token
        data = {'member_id': self.user_member_id,
                'title': '借钱实现财富自由',
                'amount': 2000,
                'loan_rate': 12.0,
                'loan_term': 3,
                'loan_date_type': 1,
                'bidding_days': 5}
        # 发送请求，添加项目
        response = request(method='post', url=url, json=data, headers=headers)
        res = response.json()
        # 提取项目的id给审核的用例使用
        self.loan_id = jsonpath.jsonpath(res, '$..id')[0]

    @data(*cases)
    def test_audit(self, case):
        # 第一步：准备数据
        url = conf.get('env', 'service') + case['url']
        # 判断是否提取审核通过的id
        if '#pass_loan_id#' in case['data']:
            case['data'] = case['data'].replace('#pass_loan_id#', str(self.pass_loan_id))
        data = eval(case['data'].replace('#loan_id#', str(self.loan_id)))
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.admin_token
        method = case['method']
        excepted = eval(case['expected'])
        # 第二步：调用接口，获取实际结果
        response = request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        if case['title'] == '审核通过' and res['msg'] == 'OK':
            # 第一次执行通过审核通过的生成类属性
            TestAudit.pass_loan_id = data['loan_id']
        # 第三步：断言
        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            result = 'Pass'
            # 判断是否需要进行sql校验
            if case['check_sql']:
                sql = case['check_sql'].replace('#loan_id#', str(self.loan_id))
                status = self.db.find_one(sql)['status']
                self.assertEqual(excepted['status'], status)
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
