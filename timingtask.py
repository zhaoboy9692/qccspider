#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2019-06-20 09:48
@Author  : Xincheng.Zhao
@Desc    :
@Email   : zhaoboy9692@163.com
@File    : timingtask.py
"""
from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler

from common.utils import creat_url
from getnewdata import new_enterprise_main


def rangeSumBST(self, root, L: int, R: int) -> int:
    if not root:
        return 0
    if L <= root.val <= R:
        return root.val + self.rangeSumBST(root.left, L, R) + self.rangeSumBST(root.right, L,R)
    elif root.val < L:
        return self.rangeSumBST(root.left, L, R)
    else:
        return self.rangeSumBST(root.right, L, R)


def task():
    creat_url()  # 创建url
    sleep(60 * 30)
    new_enterprise_main()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(task, 'cron', hour='09', minute='52')
    scheduler.start()
