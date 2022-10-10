#!/usr/bin/python
# encoding=utf-8
""" Can only be modified by the administrator. Only Path are provided.
"""
import os

# 项目目录
from utx.core.utils.tools import ReadConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件
INI_PATH = os.path.join(BASE_DIR, 'config', 'config.ini')

ini = ReadConfig(INI_PATH)

# 测试用例目录
CASE_PATH = os.path.join(BASE_DIR, 'suites', ini.getvalue('paths', 'name'))
if not os.path.exists(CASE_PATH):
    os.mkdir(CASE_PATH)
# 日志目录
LOG_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
# 安装包目录
PACKAGES_PATH = os.path.join(BASE_DIR, 'packages')
if not os.path.exists(PACKAGES_PATH):
    os.mkdir(PACKAGES_PATH)
# allure报告目录
ALLURE_REPORT_PATH = os.path.join(BASE_DIR, 'report')
if not os.path.exists(ALLURE_REPORT_PATH):
    os.mkdir(ALLURE_REPORT_PATH)

# airtest报告目录
AIRTEST_REPORT_PATH = os.path.join(BASE_DIR, 'report', 'airtest')
if not os.path.exists(AIRTEST_REPORT_PATH):
    os.mkdir(AIRTEST_REPORT_PATH)

if __name__ == '__main__':
    print(ini.getvalue('app_info', 'package'))
