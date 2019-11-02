#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019-06-19 14:28
@Author  : Xincheng.Zhao
@Desc    : 获取企业的更多信息
@Email   : zhaoboy9692@163.com
@File    : getmoredata.py
"""
import threading
from time import sleep

import requests
from lxml import etree

from common.utils import connect_redis

header = {
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36',
    'Cookie': 'zg_did=%7B%22did%22%3A%20%2216b36c370bb74c-04b786bd0af0e3-37677e03-1fa400-16b36c370bca4c%22%7D; UM_distinctid=16b36c371b5270-0019cf0e558dc2-37677e03-1fa400-16b36c371b6b60; _uab_collina=155999190721610417863548; acw_tc=015101ce15599919073061025ebad2c614d006d9e341716cae782cf82f; QCCSESSID=t928pnbf150ocj2b3dnmjlloq1; hasShow=1; CNZZDATA1254842228=194992430-1559989436-https%253A%252F%252Fwww.google.com%252F%7C1560486338; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1560473028,1560481011,1560481048,1560489256; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201560489255681%2C%22updated%22%3A%201560490141810%2C%22info%22%3A%201559991906507%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.google.com%22%2C%22cuid%22%3A%20%2236e2558b2d4f4a46cf9debb24d761546%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1560490142',
    'Referer': 'https://www.qichacha.com/'
}


def get_more_data_main():
    """
    这里可以开并发加代理，没用好的代理源暂时放弃
    :return:
    """
    r = connect_redis(0, 110)
    for key in r.keys():
        data = eval(r.get(key))
        threading.Thread(target=get_more_data, args=(key, r, data)).start()
        sleep(5)


def get_more_data(key, r, data):
    """
    根据key获取企业的经营范围和起止时间
    :param key:
    :param r:
    :param data:
    :return:
    """
    res = requests.get('https://m.qichacha.com/firm_06e4da98470faa3ab42be2b5b63f71a7.html', headers=header)
    html = etree.HTML(res.text)
    scope_list = html.xpath('//*[@id="base"]/div[2]/div[6]/div[2]/text()')
    scope = str(scope_list[0]).strip().replace('\n', '')
    start_end_time = html.xpath('//*[@id="base"]/div[2]/div[8]/div[2]/text()')
    start_time, end_time = tuple(str(start_end_time[0]).strip().replace(' ', '').split('至'))
    data['Scope'] = scope
    data['TermStart'] = start_time
    data['TeamEnd'] = end_time
    r.set(key, str(data))


if __name__ == '__main__':
    get_more_data_main()
