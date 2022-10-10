#!/usr/bin/python
# encoding=utf-8

""" Can only be modified by the administrator. Only fixtures are provided.
"""

import pytest

from logging import getLogger
from airtest.core.helper import ST
from utx.core.utils.hook import app_fixture, app_info
from config.conf import *
from run import cli_device, cli_platform, cli_wda, cli_init

logger = getLogger(__name__)
logger.info("Get PROJECT_ROOT: {}".format(ST.PROJECT_ROOT))
app_filepath = PACKAGES_PATH + '/' + ini.getvalue('app_info', 'filename')
app_name = ini.getvalue('app_info', 'package')

device_uri, device_idx, is_init = app_info(cli_platform=cli_platform, cli_device=cli_device, cli_wda=cli_wda,
                                           cli_init=cli_init,
                                           ini_platform=ini.getvalue('device_info', 'platform'),
                                           ini_device=ini.getvalue('device_info', 'device'),
                                           ini_wda=ini.getvalue('device_info', 'wda'),
                                           ini_init=ini.getvalue('device_info', 'init'))


@pytest.fixture(scope="session", autouse=True)
def app_init(request):
    app_fixture(request, device_uri=device_uri, app_filepath=app_filepath, app_name=app_name, device_idx=device_idx,
                init=is_init)
