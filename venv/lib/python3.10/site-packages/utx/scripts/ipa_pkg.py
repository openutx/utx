#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2022/2/8 10:58 上午
@Desc    :  ipa_pkg line.
"""
import os
import shutil

from utx.core.utils.tools import decryption


def pkg(wda_home, ipa_home):
    """
    mac 打包utx.ipa包
    :param wda_home: 克隆到本地 https://github.com/openutx/utx-wda.git
    :param ipa_home: ipa目录
    :return:
    """
    if os.path.exists(ipa_home):
        shutil.rmtree(ipa_home)
    os.makedirs(ipa_home)
    cmd = f"""
    cd {wda_home} &&
    xcodebuild build-for-testing -scheme WebDriverAgentRunner -sdk iphoneos -configuration Release -derivedDataPath {ipa_home}
    cd {ipa_home}/Build/Products/Release-iphoneos
    mkdir Payload && mv *.app Payload
    zip -r UTX-Runner.ipa Payload
    mv *.ipa {os.getcwd()}
    """
    os.system(cmd)
    os.system('{} parse UTX-Runner.ipa'.format(decryption(b'dGlkZXZpY2U=')))
