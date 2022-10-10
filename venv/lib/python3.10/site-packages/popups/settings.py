#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2022/2/9 4:49 下午
@Desc    :  settings line.
"""


class Settings(object):
    TPL_DIR = None
    TIMEOUT = 5
    INTERVAL = 2.0
    ENABLE = False
    APP = False
    SYS = False
    LOOP = 1
    iOS = False
    PROXY = False
    DEFAULT_ACCEPT_BUTTONS = [
        "使用App时允许", "无线局域网与蜂窝网络", "好", "稍后", "稍后提醒", "确定", "允许访问所有照片",
        "允许", "以后", "打开", "录屏", "Allow", "OK", "YES", "Yes", "Later", "Close"
    ]
