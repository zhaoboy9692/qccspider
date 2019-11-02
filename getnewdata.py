#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019-06-18 17:57
@Author  : Xincheng.Zhao
@Desc    : 获取每天新增企业
@Email   : zhaoboy9692@163.com
@File    : getnewdata.py
"""
import threading
from multiprocessing import Process
from time import sleep

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from common.utils import connect_redis, get_yesterday, read_data, more_get_token, write_data

device_id, tim, sign, header = more_get_token()

is_break = False


def new_enterprise_main():
    """
    获取新增企业数据
    :return:
    """
    global device_id, tim, sign, header
    device_id, tim, sign, header = more_get_token()
    r = connect_redis(0, 110)
    for url, city, province in creat_url():
        handle_page(url, city, province, r)
        sleep(1.5)



def handle_page(url, city, province, r):
    """
    处理每一个页面的url以及数据
    :param url:
    :param city:
    :param province:
    :param r:
    :return:
    """
    global device_id, tim, sign, header, is_break
    res = requests.get(url, headers=header)
    res_data = dict(eval(res.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')))
    if '200' not in str(res_data):
        while '200' not in str(res_data):
            sleep(10)
            sign_tmp = sign
            tim_tmp = tim
            print('handle_page', res.text)
            print('权限不足或者accessToken失效，sign失败')
            device_id, tim, sign, header = more_get_token()
            url = url.replace(sign_tmp, sign).replace().replace(tim_tmp, tim)
            res = requests.get(url, headers=header, timeout=10)
            res_data = dict(eval(res.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')))
    res.close()
    try:
        qiye_data = res_data.get('result').get('Result')
    except Exception as e:
        print(e)
        return
    if not qiye_data:
        is_break = True
        return
    write_list = []
    for qiye in qiye_data:
        if qiye.get('StartDate') != get_yesterday():
            is_break = True
            continue
        qiye['City'] = city
        qiye['Province'] = province
        del qiye['ImageUrl']
        del qiye['HitReason']
        write_list.append(qiye)
        r.set(province + ":" + city + ':' + qiye.get('KeyNo'), str(qiye))
    threading.Thread(target=write_data, args=(get_yesterday() + "-data.txt", write_list)).start()


def creat_url():
    """
    生产url
    :return:
    """
    global is_break
    for city_data in read_data('other/city_code.txt'):
        page_index = 0
        city_data = eval(city_data)
        while True:
            if is_break:
                is_break = False
                break
            page_index += 1
            url = 'https://appv3.qichacha.net/app/v1/base/getNewCompanys?province=' + str(
                city_data['provinceCode']) + '&cityCode=' + str(
                city_data['Value']) + '&pageIndex=' + str(
                page_index) + '&timestamp=' + str(tim) + '&sign=' + sign + '&platform=other&app_channel=qq'
            yield url, city_data['Desc'], city_data['provinceName']


def main():
    print(get_yesterday(), 'start')
    Process(target=new_enterprise_main).start()


if __name__ == '__main__':
    main()
    scheduler = BlockingScheduler()
    # 每天凌晨1点执行脚本
    scheduler.add_job(main, 'cron', hour='01', minute='01')
    scheduler.start()
