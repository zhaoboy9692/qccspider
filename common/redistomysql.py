#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.

@Time    : 2019-06-16 20:37
@Author  : Xincheng.Zhao
@Desc    :
@Email   : zhaoboy9692@163.com
@File    : redistomysql.py
"""
import sys

import pymysql

from redisutils import r, r1, r3
from utils import read_data, cpca_data

conn = pymysql.Connect(host='127.0.0.1', port=3306, user='qidatas', password='KJsniAyhjfzENZG6',
                       database='qidatas')
cursor = conn.cursor()


def sql_ex(sql, data):
    conn = pymysql.Connect(host='127.0.0.1', port=3306, user='qidatas', password='KJsniAyhjfzENZG6',
                           database='qidatas')
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()


def sql_many_ex(sql, datas):
    conn = pymysql.Connect(host='127.0.0.1', port=3306, user='qidatas', password='KJsniAyhjfzENZG6',
                           database='qidatas')
    cursor = conn.cursor()
    cursor.executemany(sql, datas)
    conn.commit()


# 插入省份 "INSERT INTO Province(code,pname) values (%(province)s,%(name)s)"
# 插入城市 "INSERT INTO city(id,city_name,p_code,p_name) values (%(Value)s,%(Desc)s,%(provinceCode)s,%(provinceName)s)"

if __name__ == '__main__':
    sql = "REPLACE INTO qidata(KeyNo,Name,CreditCode,StartDate,Address,RegistCapi,ShortStatus,City,Province,EconKind,OperName,Scope,SubIndustry,TermStart,TeamEnd,OrgNo,BelongOrg,phone,ImageUrl,EndDate,IsOnStock,county,Partnersid,Email) values (%(KeyNo)s,%(Name)s,%(CreditCode)s,%(StartDate)s,%(Address)s,%(RegistCapi)s,%(ShortStatus)s,%(City)s,%(Province)s,%(EconKind)s,%(OperName)s,%(Scope)s,%(SubIndustry)s,%(TermStart)s,%(TeamEnd)s,%(OrgNo)s,%(BelongOrg)s,%(phone)s,%(ImageUrl)s,%(EndDate)s,%(IsOnStock)s,%(county)s,%(Partnersid)s,%(Email)s)"
    datas = []
    i = 0
    for key in r1.keys():
        i += 1
        data = r1.get(key)
        data = eval(data)
        key = str(key, encoding='utf8')
        province, city, county = cpca_data(data.get('Address'))
        data['county'] = county
        data['KeyNo'] = data.get('KeyNo') if data.get('KeyNo') else key[key.find(':') + 1:]
        data['EconKind'] = data.get('EconKind')
        data['Scope'] = data.get('Scope')
        data['SubIndustry'] = data.get('SubIndustry')
        data['TermStart'] = data.get('TermStart')
        data['TeamEnd'] = data.get('TeamEnd')
        data['OrgNo'] = data.get('OrgNo')
        data['BelongOrg'] = data.get('BelongOrg')
        data['City'] = data.get('City') if data.get('City') else city
        data['Province'] = data.get('Province') if data.get('Province') else province
        data['phone'] = data.get('ContactNumber')
        data['ImageUrl'] = data.get('ImageUrl')
        data['EndDate'] = data.get('EndDate')
        data['IsOnStock'] = data.get('IsOnStock')
        data['Partnersid'] = data.get('Partnersid')
        data['Email'] = data.get('Email')
        print(i)
        datas.append(data)
        if i % 50000 == 0:
            sql_many_ex(sql, datas)
            datas.clear()
    sql_many_ex(sql, datas)
