#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.

@Time    : 2019-06-18 17:31
@Author  : Xincheng.Zhao
@Desc    : 企查查爬虫通用类
@Email   : zhaoboy9692@163.com
@File    : utils.py
"""
import datetime
import hashlib
import json
import random
import time
from time import sleep

import redis
import requests


def write_data(file_name, data, mode='a'):
    """
    写入文件
    :param file_name:
    :param data:要写入的数据 list
    :param mode: 读写类型
    :return:
    """
    with open(file_name, mode, encoding='utf8') as file:
        for code in data:
            file.write(str(code) + '\n')


def read_data(file_name):
    """
    读取文件
    :param file_name: 要读文件名
    :return:
    """
    with open(file_name, 'r', encoding='utf8') as file:
        for data in file.readlines():
            yield str(data).replace('\n', '')


def ref_access_token():
    """
    刷新access_token
    :return:
    """
    global stop_ref
    stop_ref = False
    url = 'https://appv3.qichacha.net/app/v1/admin/refreshToken'
    r2 = connect_redis(2, 1)
    post_data = {
        'appId': r2.get('appId'), 'deviceId': r2.get('deviceId'), 'version': r2.get('version'),
        'deviceType': 'android', 'os': '', 'timestamp': r2.get('timestamp'),
        'refreshToken': r2.get('refreshToken'),
        'sign': r2.get('sign'), 'platform': 'other', 'app_channel': 'qq'
    }
    res = requests.post(url, data=post_data)
    print(res.text)
    if '请重新登录' in str(res.text):
        res = requests.post(url, data=post_data)
        while '请重新登录' in str(res.text):
            print('通知')
            res = requests.post(url, data=post_data)
            while not send_validate():
                sleep(120)
            sleep(60 * 30)
    access_token = 'Bearer ' + eval(res.text)['result']['access_token']
    r2.set('access_token', str({'access_token': access_token}))
    return access_token


def connect_redis(db=0, connect_num=110):
    """
    连接redis
    :param db: 第几个db,0,1,2,3
    :param connect_num: 连接数量
    :return:
    """
    return redis.Redis(
        connection_pool=redis.ConnectionPool(host='132.232.11.246', port=6379, db=int(db), max_connections=connect_num,
                                             password='zxc199692'))


def login():
    """
    登录
    :return:
    """
    header = {
        'Authorization': 'NmY0MzZkMTUwZWEzNDFiZmU2MmJmODYyNTUzYmNhZjc',
        'User-Agent': 'okhttp/3.11.0'
    }
    url = 'https://appv3.qichacha.net/app/v1/admin/login'
    post_data = {
        'loginType': 2, 'accountType': 1, 'account': 17115610599,
        # fjf95915
        'password': '3a9505bbacc13fda0c3f82a0de6fce32', 'identifyCode': '', 'key': '', 'token': '',
        'deviceToken': 'Atuyo-ECfQgBB3a-TIxGDyDJgBpVSVD9ecNzsEkQoDZc',
        'internationalCode': '+86', 'timestamp': '1560833916138', 'sign': '3cda9299c766b50ec987355c3002a89d98d2cf5e',
        'platform': 'other', 'app_channel': 'qq'
    }
    res = requests.post(url, data=post_data, headers=header)
    if '200' not in str(res.text):
        res = requests.post(url, data=post_data, headers=header)
    print(res.text)
    return json.loads(res.text)


def get_access_token():
    """
    登录时候要获取的access_token
    :return:
    """
    url = 'https://appv3.qichacha.net/app/v1/admin/getAccessToken'
    # post_data = {
    #     'appId': '80c9ef0fb86369cd25f90af27ef53a9e', 'deviceId': 'XPptnO4q4ogDAHWxD4pGBAA2', 'version': '12.2.4',
    #     'deviceType': 'android', 'os': '', 'timestamp': '1560479991510',
    #     'sign': '14b767ef42391343f0547f9a53dfda36b7e1f855', 'platform': 'other', 'app_channel': 'qq'
    # }
    r2 = connect_redis(2, 1)
    post_data = {
        'appId': r2.get('appId'), 'deviceId': r2.get('deviceId'), 'version': r2.get('version'),
        'deviceType': 'android', 'os': '', 'timestamp': r2.get('timestamp'),
        'refreshToken': r2.get('refreshToken'),
        'sign': r2.get('sign'), 'platform': 'other', 'app_channel': 'qq'
    }
    res = requests.post(url, data=post_data)
    print(res.text)
    return eval(res.text)['result']['access_token']


def creat_url():
    """
    生产每天的url
    :return:
    """
    r2 = connect_redis(2, 110)
    sign = str(r2.get('sign'), encoding='utf8')
    timestamp = str(r2.get('timestamp'), encoding='utf8')
    for city_data in read_data('../other/city_code.txt'):
        page_index = 0
        city_data = eval(city_data)
        while page_index < 55:
            page_index += 1
            url = 'https://appv3.qichacha.net/app/v1/base/getNewCompanys?province=' + str(
                city_data['provinceCode']) + '&cityCode=' + str(
                city_data['Value']) + '&pageIndex=' + str(
                page_index) + '&timestamp=' + timestamp + '&sign=' + sign + '&platform=other&app_channel=qq'
            m5 = hashlib.md5()
            m5.update(url.encode(encoding='utf8'))
            print(m5.hexdigest())
            r2.set('url-' + str(city_data['provinceName']) + ":" + str(
                city_data['Desc']) + ':' + str(m5.hexdigest()),
                   url)


def get_yesterday():
    """
    获取昨天的日期
    :return:
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday.strftime("%Y-%m-%d")


def send_validate():
    """
    每天短信通知接口，虽然是验证码
    :return:
    """
    url = 'http://m.310win.com/Trade/Mine/User/UserHandler.ashx?n=' + str(random.random())
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Cookie': 'ASP.NET_SessionId=nppg4umjj11qenr2hc31x2rq',
        'Origin': 'http://m.310win.com',
        'Referer': 'http://m.310win.com',
    }
    r2 = connect_redis(2, 1)
    post_data = {
        'action': 'smscodebyreg',
        'tk': '636965669256109694', 'username': '15702980078'
    }
    res = requests.post(url, data=post_data, headers=header)
    if json.loads(res.text)['ErrCode'] != 0:
        return False
    return True


if __name__ == '__main__':
    print(time.localtime())
    print(creat_url())
    print(time.localtime())
