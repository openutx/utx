#!/usr/bin/python
# encoding=utf-8
""" Can only be modified by the administrator. Only Runner are provided.
"""
import os
import pytest
from utx.cli.cli import cli_env

from config.conf import ALLURE_REPORT_PATH
from utx.core.utils.tools import allure_report

cli_device, cli_platform, cli_wda, cli_init = cli_env()

if __name__ == '__main__':
    report_path = ALLURE_REPORT_PATH + os.sep + "result"
    report_html_path = ALLURE_REPORT_PATH + os.sep + "html"
    pytest.main(["-s", "--alluredir", report_path, "--clean-alluredir"])
    allure_report(report_path, report_html_path)
