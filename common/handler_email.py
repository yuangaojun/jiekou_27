# -*- coding:utf-8 -*-
"""
==============================
Author:yuan
Time  :2020/4/10 11:50
file  :handler_email.py
===============================
"""
'''
service:smtp.qq.com
port:465
musen_nmb@qq.com
algmmzptupjccbab
'''
import smtplib
import os
from common.handler_path import REPORT_DIR
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_eamil():
    # 连接邮箱服务器
    smtp = smtplib.SMTP_SSL(host='smtp.qq.com',port='465')
    # 登录邮箱
    smtp.login(user='musen_nmb@qq.com',password='algmmzptupjccbab')

    # # 读取邮件的内容，作为正文发送过去（缺陷：邮件中显示不友好）
    # with open(os.path.join(REPORT_DIR,'report.html'),'rb') as f:
    #     content = f.read()
    # msg = MIMEText(content,_subtype='html', _charset='utf8')

    # 创建一个多组件的邮件
    msg = MIMEMultipart()
    msg['Subject'] = '邮件主题'
    msg['To'] = '发件人'
    msg['From'] = '收件人'
    # 构建邮件中的文本
    text = MIMEText('邮件中的文本内容',_charset='utf-8')
    msg.attach(text)

    # 构造邮件附件
    with open(os.path.join(REPORT_DIR,'report.html'),'rb') as f:
        content = f.read()
    report = MIMEApplication(content)
    report.add_header('content-disposition', 'attachment', filename='python.html')
    msg.attach(report)

    # 发送邮件
    smtp.send_message(msg,from_addr='musen_nmb@qq.com',to_addrs='771305126@qq.com')



if __name__ == '__main__':
    send_eamil()

