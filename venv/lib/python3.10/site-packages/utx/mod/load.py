#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2021/12/8 5:59 下午
@Desc    :  plugins line.
"""

import traceback
import importlib

from airtest.utils.logger import get_logger

LOGGING = get_logger(__name__)


class TestPlugin:
    @staticmethod
    def show_me():
        print('plugin_name')


def plugin(plugin_name: str, sep=':'):
    """

    :param plugin_name:
    :param sep:
    :return:
    """
    m, _, c = plugin_name.partition(sep)
    mod = importlib.import_module(m)
    cls = getattr(mod, c)
    return cls()


def init_plugin_modules(plugins):
    """
    动态导入插件
    :param plugins:
    :return:
    """
    if not plugins:
        return
    for plugin_name in plugins:
        LOGGING.debug("try loading plugin: %s" % plugin_name)
        try:
            __import__(plugin_name)
        except ImportError:
            LOGGING.error(traceback.format_exc())


if __name__ == '__main__':
    pg = plugin('_load:TestPlugin')
    pg.show_me()
