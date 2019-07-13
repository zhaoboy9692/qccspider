#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019-06-18 17:57
@Author  : Xincheng.Zhao
@Desc    : 获取每天新增企业
@Email   : zhaoboy9692@163.com
@File    : getnewdata.py
"""
from time import sleep

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from common.utils import connect_redis, get_yesterday, read_data, more_get_token

device_id, tim, sign, header = more_get_token()


def new_enterprise_main():
    """
    获取新增企业数据
    :return:
    """
    r = connect_redis(0, 110)
    for url, city, province in creat_url():
        handle_page(url, city, province, r)
    print(get_yesterday(), 'end')


def handle_page(url, city, province, r):
    """
    处理每一个页面的url以及数据
    :param url:
    :param city:
    :param province:
    :param r:
    :return:
    """
    global device_id, tim, sign, header
    res = requests.get(url, headers=header)
    print(city, province)
    res_data = dict(eval(res.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')))
    if '200' not in str(res_data):
        while '200' not in str(res_data):
            sleep(10)
            print('handle_page', res.text)
            print('权限不足或者accessToken失效，sign失败')
            device_id, tim, sign, header = more_get_token()
            res = requests.get(url, headers=header, timeout=10)
            res_data = dict(eval(res.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')))
    res.close()
    try:
        qiye_data = res_data.get('result').get('Result')
    except Exception as e:
        print(e)
        return
    for qiye in qiye_data:
        if qiye.get('StartDate') != get_yesterday(): continue
        qiye['City'] = city
        qiye['Province'] = province
        r.set(province + city + ':' + qiye.get('KeyNo'), str(qiye))


def creat_url():
    """
    生产url
    :return:
    """
    for city_data in read_data('other/city_code.txt'):
        page_index = 0
        city_data = eval(city_data)
        while page_index < 55:
            page_index += 1
            url = 'https://appv3.qichacha.net/app/v1/base/getNewCompanys?province=' + str(
                city_data['provinceCode']) + '&cityCode=' + str(
                city_data['Value']) + '&pageIndex=' + str(
                page_index) + '&timestamp=' + str(tim) + '&sign=' + sign + '&platform=other&app_channel=qq'
            yield url, city_data['Desc'], city_data['provinceName']


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # 每天执行时间,定点执行
    scheduler.add_job(new_enterprise_main, 'cron', hour='19', minute='24')
    scheduler.start()
