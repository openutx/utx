#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2021/12/11 11:14 上午 
@Desc    :  pg_1 line.
"""
from utx.mod.platform import PluginsProcessor


@PluginsProcessor.plugin_register('pg1')
class CleanMarkdownBolds(object):
    @staticmethod
    def process(text):
        return text.replace('**', '')
