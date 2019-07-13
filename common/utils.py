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
import time

import execjs
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


def connect_redis(db=0, connect_num=110):
    """
    连接redis
    :param db: 第几个db,0,1,2,3
    :param connect_num: 连接数量
    :return:
    """
    return redis.Redis(
        connection_pool=redis.ConnectionPool(host='132.232.11.246', port=6379, db=int(db), max_connections=connect_num,
                                             password='cwx1995'))


def get_yesterday():
    """
    获取昨天的日期
    :return:
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday.strftime("%Y-%m-%d")


def more_get_token():
    device_id = execjs.compile(
        'function guid() {for (var e = "", n = 1; n <= 32; n++) {var t = Math.floor(16 * Math.random()).toString(16);'
        'e += t, 8 != n &&12 != n && 16 != n && 20 != n || (e += "-")}return e}').call('guid')
    md5 = hashlib.md5()
    tim = int(time.time())
    md5.update(bytes(device_id + str(tim) + '这里的key值请关注【小白技术社】留言获取', encoding='utf8'))
    sign = md5.hexdigest()
    url_get_acc = 'https://appv3.qichacha.net/app/v1/admin/getAccessToken'
    post_data_acc = {"deviceType": 'quickApp', 'os': "quickApp", 'sign': sign,
                     'appId': "ec11c16358b011e89f066c92bf2c15cd", 'deviceId': device_id,
                     'version': '11.2.0', 'account': '', 'timestamp': tim}
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; 16th Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36 hap/1.4/meizu com.meizu.flyme.directservice/2.5.16-1048 com.qichacha.quickapp/1.0.3 ({"packageName":"com.meizu.flyme.launcher","type":"3rd_part","extra":{}})',
        'Referer': 'https://www.qichacha.cn',
        'Origin': 'https://www.qichacha.cn',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    res = requests.post(url_get_acc, data=post_data_acc, headers=header)
    access_token = eval(res.text).get('result').get('access_token')
    header['authorization'] = 'Bearer ' + access_token

    return device_id, tim, sign, header
