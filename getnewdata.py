#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019-06-18 17:57
@Author  : Xincheng.Zhao
@Desc    : 获取每天新增企业
@Email   : zhaoboy9692@163.com
@File    : getnewdata.py
"""
import queue
import threading
from time import sleep

import requests

from common.utils import connect_redis, ref_access_token, get_yesterday

header = {
    'Authorization': eval(connect_redis(2).get('access_token'))['access_token'],
    'User-Agent': 'okhttp/3.11.0'
}


def put_queue(r2, q):
    """
    塞入队列
    :param r2:
    :param q:
    :return:
    """
    for key in r2.keys('url-*'):
        key_list = str(key, encoding='utf8').replace('url-', '').split(':')
        q.put({'city': key_list[0], 'province': key_list[1], 'url': r2.get(key), 'key': key})


def new_enterprise_main():
    r2 = connect_redis(2)
    r = connect_redis(0, 110)
    q = queue.Queue(20)
    threading.Thread(target=put_queue, args=(r2, q)).start()
    sleep(5)
    print(q.empty())
    while not q.empty():
        handle_page(q, r2, r)
        sleep(1.5)
    print(get_yesterday(), 'end')


def handle_page(q, r2, r):
    """
    处理每一个页面的
    :param q:
    :param r2:
    :param r:
    :return:
    """
    q_page = q.get()
    city = q_page['city']
    key = q_page['key']
    province = q_page['province']
    url = q_page['url']
    res = requests.get(url, headers=header)
    print(res.text)
    res_data = dict(eval(res.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')))
    if '200' not in str(res_data):
        print('权限不足或者accessToken失效，sign失败')
        header['Authorization'] = ref_access_token()
        sleep(5)
        res = requests.get(url, headers=header, timeout=10)
        res_data = dict(eval(res.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')))
    res.close()
    try:
        qiye_data = res_data.get('result').get('Result')
        print(city, province)
    except Exception as e:
        return
    for qiye in qiye_data:
        if qiye.get('StartDate') != get_yesterday(): continue
        qiye['City'] = city
        qiye['Province'] = province
        r.set(province + city + qiye.get('KeyNo'), str(qiye))
    print(key)
    r2.delete(key)


if __name__ == '__main__':
    new_enterprise_main()
