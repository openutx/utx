#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2022/2/9 2:40 下午
@Desc    :  dismiss line.
"""

from airtest.core.api import *
from popups.settings import Settings as UT
from loguru import logger


def popup(devices=None):
    """
    General pop-up processing!
    :param devices: Current device uri
    :return: Click pop-up event
    """
    if UT.ENABLE:
        if devices:
            auto_setup(__file__, devices=str(devices).split(','))
        else:
            auto_setup(__file__)
        ST.FIND_TIMEOUT_TMP = UT.TIMEOUT

        if UT.SYS:
            if UT.iOS:
                ios = device()
                for step in range(UT.LOOP):
                    for btn in UT.DEFAULT_ACCEPT_BUTTONS:
                        logger.info(f'Try to find button: {btn}')
                        with ios.alert_watch_and_click([btn], interval=UT.INTERVAL):
                            sleep(1)
            else:
                if UT.TPL_DIR:
                    images_path = UT.TPL_DIR
                else:
                    images_path = str(__file__).replace('dismiss.py', 'tpl/sys/android')
                try:
                    images = sorted([tpl for tpl in os.listdir(images_path) if str(tpl).endswith('png')])
                    logger.info(f'Try to find template pictures: {images}')
                    for step in range(UT.LOOP):
                        for img in images:
                            logger.info(f'Try to find tpl: {img}')
                            pos = exists(Template(r"{}/{}".format(images_path, img)))
                            if pos:
                                touch(pos)
                except TargetNotFoundError as E:
                    logger.warning(f'Picture template path does not exist: {images_path}')
                    logger.error(f'{E}')
        elif UT.APP:
            if UT.TPL_DIR:
                images_path = UT.TPL_DIR
            else:
                images_path = str(__file__).replace('dismiss.py', 'tpl/app')
            try:
                images = sorted([tpl for tpl in os.listdir(images_path) if str(tpl).endswith('png')])
                logger.info(f'Try to find template pictures: {images}')
                for step in range(UT.LOOP):
                    for img in images:
                        logger.info(f'Try to find tpl: {img}')
                        pos = exists(Template(r"{}/{}".format(images_path, img)))
                        if pos:
                            touch(pos)
            except TargetNotFoundError as E:
                logger.warning(f'Picture template path does not exist: {images_path}')
                logger.error(f'{E}')
