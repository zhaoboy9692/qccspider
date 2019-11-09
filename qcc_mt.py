#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019-11-09 11:44
@Author  : Xincheng.Zhao
@Desc    :
@Email   : zhaoboy9692@163.com
@File    : qcc_mt.py
"""

import mitmproxy.http
from mitmproxy import ctx


class Demo(object):
    def __init__(self):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        # 过滤非企查查接口地址
        if flow.request.host != "appv3.qichacha.net":
            return
        ctx.log.info(f"sign is: {flow.request.query.get('sign')},时间戳 is: {flow.request.query.get('timestamp')}")


addons = [
    Demo()
]
