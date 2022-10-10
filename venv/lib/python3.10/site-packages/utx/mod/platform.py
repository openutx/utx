#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2021/12/11 11:11 上午 
@Desc    :  platform line.
"""


class PluginsProcessor(object):
    PLUGINS = {}

    def process(self, text, plugins=()):
        if plugins is ():
            for plugin_name in self.PLUGINS.keys():
                text = self.PLUGINS[plugin_name]().process(text)
        else:
            for plugin_name in plugins:
                text = self.PLUGINS[plugin_name]().process(text)
        return text

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name: plugin})
            return plugin

        return wrapper
