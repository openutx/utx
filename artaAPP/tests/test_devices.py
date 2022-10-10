#!/usr/bin/python
# encoding=utf-8
""" Can only be modified by the administrator. Only Cases are provided.
"""

import allure
import pytest
from utx.core.css.custom_report import gen_report
from utx.core.utils.tools import decryption, selector_v2, str_to_bool

from config.conf import *
from conftest import device_uri
from utx.core.utils.runner import run_air

device_address = device_uri
results = []
result_list = []

status = str_to_bool(ini.getvalue('mode', 'is_all'))
record = str_to_bool(ini.getvalue('mode', 'record'))
flag = ini.getvalue('suites', 'cases')
app_name = ini.getvalue('app_info', 'package')
times = int(ini.getvalue('reruns', 'times'))
cases = selector_v2(path=CASE_PATH, status=status, mark=flag)


@allure.feature("APP automation test")
class TestApp:
    @pytest.mark.flaky(reruns=times)
    @pytest.mark.parametrize("url", device_address)
    @pytest.mark.parametrize("case", cases)
    @allure.story("APP automation test")
    @allure.title("Current device:{url},Running case:{case}")
    @allure.description("APP automation test")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("Smoke testing")
    def test_ui_app(self, url, case):
        device_url = url
        result, dev = run_air(devices=device_url, case=case, app_name=app_name, log_path=LOG_PATH, case_path=CASE_PATH,
                              base_dir=BASE_DIR, record=record,
                              static_dir=decryption('aHR0cHM6Ly9mYXN0bHkuanNkZWxpdnIubmV0L2doL29wZW51dHgvc3RhdGljLw=='))
        result_list.append(result)
        summary_info = {'devices': dev, 'result': result_list}
        results.append(summary_info)
        assert result['result'] is True

    @allure.story("APP automation test")
    @allure.title("Generate test report of running device")
    @allure.description("APP automation test")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("Generate report")
    def test_report(self):
        gen_report(results=results, report_path=AIRTEST_REPORT_PATH)


if __name__ == "__main__":
    pytest.main(["-s", "test_devices.py"])
