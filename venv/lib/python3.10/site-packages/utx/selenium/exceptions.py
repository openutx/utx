#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  11/02/2021 8:16 PM
@Desc    :  exceptions line.
"""

from __future__ import unicode_literals

import utx.selenium.utils.six as six


def to_text(val):
    if not isinstance(val, six.text_type):
        return val.decode('utf-8')
    return val


class AirtestSeleniumException(Exception):
    """
    Base class for errors and exceptions of Airtest-Selenium
    """

    def __init__(self, message=None):
        super(AirtestSeleniumException, self).__init__(message)
        self.message = message

    def __str__(self):
        if six.PY2:
            if isinstance(self.message, six.text_type):
                return self.message.encode("utf-8")
            else:
                return self.message
        else:
            if isinstance(self.message, bytes):
                return self.message.decode('utf-8')
            else:
                return self.message

    __repr__ = __str__


class IsNotTemplateError(AirtestSeleniumException):
    """
    Base class for errors and exceptions of Airtest-Selenium
    """

    def __init__(self, message=None):
        super(IsNotTemplateError, self).__init__(message)

    def __str__(self):
        if six.PY2:
            if isinstance(self.message, six.text_type):
                return self.message.encode("utf-8")
            else:
                return self.message
        else:
            if isinstance(self.message, bytes):
                return self.message.decode('utf-8')
            else:
                return self.message

    __repr__ = __str__
