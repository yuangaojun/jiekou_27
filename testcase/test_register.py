# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/3/20 21:56
file  :test_register.py
===============================
"""
import unittest
import requests
import os
import random
from common.handler_logging import log
from library.myddt import ddt, data
from common.handler_doexcel import DoExcle
from common.handler_config import conf
from common.handler_path import DATA_DIR
from common.handler_db import HandlerMysql

filename = os.path.join(DATA_DIR, 'cases_code.xlsx')


@ddt
class RegisterTestCase(unittest.TestCase):
    '''注册接口测试用例类'''
    case_register = DoExcle(filename, 'register')
    case_data_register = case_register.read_excle_data_is_dict_02()
    db = HandlerMysql()

    @data(*case_data_register)
    def test_register(self, case):
        '''注册接口测试用例'''
        # 请求方法
        method = case['method']
        # 请求地址
        url = conf.get('env','service') + case['url']
        # 请求头
        headers = eval(conf.get('env', 'headers'))
        # 请求参数
        # 判断是否有手机号码需要替换
        if '#phone#' in case['data']:
            phone = self.random_phone()
            case['data'] = case['data'].replace('#phone#', phone)
        data = (eval(case['data']))
        response = requests.request(method=method, url=url, headers=headers, json=data)
        res = response.json()
        # 预期结果
        expected = eval(case['expected'])
        try:
            # 断言
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # 判断是否需要进行sql校验
            if case['check_sql']:
                sql = case['check_sql'].replace('#phone#',phone)
                res_sql = self.db.find_count(sql)
                self.assertTrue(1,res_sql)
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
            self.case_register.back_write(case['case_id'] + 1, 8, response.content.decode('utf-8'))
            self.case_register.back_write(case['case_id'] + 1, 9, result)

    @classmethod
    def random_phone(cls):
        '''生成一个数据库里面未注册的手机号码'''
        while True:
            phone = '135'
            for i in range(8):
                r = random.randint(0, 9)
                phone += str(r)
            sql = 'SELECT * FROM futureloan.member where mobile_phone="{}"'.format(phone)
            res = cls.db.find_count(sql)
            if res == 0:
                return phone


if __name__ == '__main__':
    unittest.main()
