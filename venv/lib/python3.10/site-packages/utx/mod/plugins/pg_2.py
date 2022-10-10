#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2021/12/11 11:15 上午 
@Desc    :  pg_2 line.
"""
from utx.mod.platform import PluginsProcessor


@PluginsProcessor.plugin_register('pg2')
class CleanMarkdownItalic(object):
    @staticmethod
    def process(text):
        return text.replace('--', '')
