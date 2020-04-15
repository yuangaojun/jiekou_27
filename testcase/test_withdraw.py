# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/29 18:58
file  :test_withdraw.py
===============================
"""

import unittest
import os
import jsonpath
import decimal
from requests import request
from library.myddt import ddt, data
from common.handler_doexcel import DoExcle
from common.handler_path import DATA_DIR
from common.handler_config import conf
from common.handler_logging import log
from common.handler_db import HandlerMysql


@ddt
class WithdrawTestCase(unittest.TestCase):
    '''提现接口测试类'''

    excel = DoExcle(os.path.join(DATA_DIR, 'cases_code.xlsx'), 'withdraw')
    case_data = excel.read_excle_data_is_dict_02()
    db = HandlerMysql()

    @classmethod
    def setUpClass(cls):
        '''提现接口测试用例类执行前提条件'''

        # 准备登录接口登录数据
        headers = eval(conf.get('env', 'headers'))
        method = conf.get('env', 'request_method')
        login_url = conf.get('env', 'service') + '/member/login'
        data = eval(conf.get('env', 'data'))
        # 登录接口
        login_request = request(method=method, headers=headers, url=login_url, json=data).json()
        # 获取登录后的token及用户id
        cls.token = 'Bearer' + ' ' + str(jsonpath.jsonpath(login_request, '$..token')[0])
        cls.member_id = str(jsonpath.jsonpath(login_request, '$..id')[0])

    @data(*case_data)
    def test_withdraw(self, case):
        '''
        提现接口测试方法
        :param case: 测试用例数据
        :return:None
        '''

        # 准备预期结果
        expected = eval(case['expected'])

        # 准备测试数据
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = self.token
        withdraw_url = conf.get('env', 'service') + case['url']
        request_method = case['method']
        # 提现之前的余额
        if case['check_sql']:
            dd_start_money = self.db.find_one(case['check_sql'].format(self.member_id))['leave_amount']
            start_money = decimal.Decimal(str(dd_start_money))
        # 判断用例提现超过可用余额时,使用数据库余额加1进行替换
        if '#greater_max_amount#' in case['data']:
            data = case['data'].replace('#member_id#', self.member_id)
            amount = start_money + 1
            # 使用最大金额+1替换掉该用例中的提现金额
            case_data = data.replace('#greater_max_amount#', str(amount))
        else:
            case_data = case['data'].replace('#member_id#', self.member_id)
        data = eval(case_data)

        # 请求提现接口，进行提现操作
        response = request(method=request_method, url=withdraw_url, headers=headers, json=data).json()

        # 提现之后的余额
        if case['check_sql']:
            db_end_money = self.db.find_one(case['check_sql'].format(self.member_id))['leave_amount']
            end_money = decimal.Decimal(str(db_end_money))

        try:
            # 断言
            self.assertEqual(expected['code'], response['code'])
            self.assertEqual(expected['msg'], response['msg'])
            # 提现未超过可用余额时断言
            if case['check_sql'] and '#greater_max_amount#' not in case['data']:
                self.assertEqual(decimal.Decimal(str(data['amount'])), start_money - end_money)
            # 提现超过可用余额时断言,
            if '#greater_max_amount#' in case['data']:
                self.assertEqual(start_money, end_money)
            result = 'Pass'
            log.error('用例名称：{}，测试结果：{}'.format(case['title'], result))
        except AssertionError as e:
            result = 'Fail'
            log.error('用例名称：{}，测试结果{}：\n{}'.format(case['title'], result, e))
            log.exception(e)
            raise e
        finally:
            self.excel.back_write(case['case_id'] + 1, 8, str(response))
            self.excel.back_write(case['case_id'] + 1, 9, result)
