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
from common.handler_data import EnvData, replace_data


@ddt
class AddTestCase(unittest.TestCase):
    '''提现接口测试类'''

    excel = DoExcle(os.path.join(DATA_DIR, 'cases_code.xlsx'), 'add')
    case_data = excel.read_excle_data_is_dict_02()
    db = HandlerMysql()

    @classmethod
    def setUpClass(cls):
        '''加标接口测试用例类执行前提条件：登录'''

        # 准备登录接口登录数据
        headers = eval(conf.get('env', 'headers'))
        method = conf.get('env', 'request_method')
        login_url = conf.get('env', 'service') + '/member/login'
        data = eval(conf.get('env', 'data'))
        # 登录接口
        login_request = request(method=method, headers=headers, url=login_url, json=data).json()
        # 获取登录后的token及用户id
        token = 'Bearer' + ' ' + str(jsonpath.jsonpath(login_request, '$..token')[0])
        setattr(EnvData, 'token', token)
        member_id = str(jsonpath.jsonpath(login_request, '$..id')[0])
        setattr(EnvData, 'member_id', member_id)

    @data(*case_data)
    def test_add(self, case):
        '''
        加标接口测试方法
        :param case: 测试用例数据
        :return:None
        '''

        # 准备预期结果
        expected = eval(case['expected'])

        # 准备测试数据
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = getattr(EnvData, 'token')
        withdraw_url = conf.get('env', 'service') + case['url']
        request_method = case['method']
        # 替换用户id
        # case_data = case['data'].replace('#member_id#', self.member_id)
        case_data = replace_data(case['data'])
        data = eval(case_data)

        # 加标之前查询数据库中该用户标的数量
        if case['check_sql']:
            # sql = case['check_sql'].replace('#member_id#',self.member_id)
            sql = replace_data(case['check_sql'])
            start_count = self.db.find_count(sql)

        # 请求加标接口，进行加标操作
        response = request(method=request_method, url=withdraw_url, headers=headers, json=data).json()

        try:
            # 断言
            self.assertEqual(expected['code'], response['code'])
            self.assertEqual(expected['msg'], response['msg'])

            # 加标之后查询数据库中该用户标的数量
            if case['check_sql']:
                # sql = case['check_sql'].replace('#member_id#', self.member_id)
                sql = replace_data(case['check_sql'])
                end_count = self.db.find_count(sql)
                self.assertEqual(1, end_count - start_count)

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


if __name__ == '__main__':
    unittest.main()
