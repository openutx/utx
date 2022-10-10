#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  8/31/2021 6:42 PM
@Desc    :  Runner line.
"""
import time
import unittest
import sys
import six
import re
import shutil
import traceback
import warnings
from io import open

from popups.dismiss import popup, UT
from airtest.core.api import G, auto_setup, log, stop_app, shell, connect_device
from airtest.core.helper import device_platform
from airtest.core.settings import Settings as ST
from airtest.utils.compat import script_dir_name, script_log_dir
from copy import copy

from argparse import *

from airtest.core.android.adb import ADB
from airtest.core.api import device, start_app
from airtest.core.error import AirtestError

from utx.core.utils.tools import ios_device_info, plat, decryption
from poco.exceptions import PocoException

from utx.core.css import report
import os


class AirtestCase(unittest.TestCase):
    PROJECT_ROOT = "."
    SCRIPTEXT = ".air"
    TPLEXT = ".png"

    @classmethod
    def setUpClass(cls):
        cls.args = args

        setup_by_args(args)

        # setup script exec scope
        cls.scope = copy(globals())
        cls.scope["exec_script"] = cls.exec_other_script

    def setUp(self):
        if self.args.log and self.args.recording:
            try:
                device().start_recording()
            except AirtestError:
                traceback.print_exc()

    def tearDown(self):
        if self.args.log and self.args.recording:
            try:
                if isinstance(self.args.recording, six.string_types) and self.args.recording.endswith(".mp4"):
                    output_name = os.path.basename(self.args.recording)
                    # output_name = dev.serialno + "_" + basename if len(G.DEVICE_LIST) > 1 else basename
                else:
                    output_name = "recording_{serialno}.mp4".format(serialno=device().serialno)
                output = os.path.join(self.args.log, output_name)
                device().stop_recording(output)
            except AirtestError:
                traceback.print_exc()

    def runTest(self):
        scriptpath, pyfilename = script_dir_name(self.args.script)
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        self.scope["__file__"] = pyfilepath
        with open(pyfilepath, 'r', encoding="utf8") as f:
            code = f.read()
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())

        try:
            exec(compile(code.encode("utf-8"), pyfilepath, 'exec'), self.scope)
        except Exception as err:
            log(err, desc="Final Error", snapshot=True)
            six.reraise(*sys.exc_info())

    @classmethod
    def exec_other_script(cls, scriptpath):
        """run other script in test script"""

        warnings.simplefilter("always")
        warnings.warn("please use using() api instead.", PendingDeprecationWarning)

        def _sub_dir_name(scriptname):
            dirname = os.path.splitdrive(os.path.normpath(scriptname))[-1]
            dirname = dirname.strip(os.path.sep).replace(os.path.sep, "_").replace(cls.SCRIPTEXT, "_sub")
            return dirname

        def _copy_script(src, dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst, ignore_errors=True)
            os.mkdir(dst)
            for f in os.listdir(src):
                srcfile = os.path.join(src, f)
                if not (os.path.isfile(srcfile) and f.endswith(cls.TPLEXT)):
                    continue
                dstfile = os.path.join(dst, f)
                shutil.copy(srcfile, dstfile)

        # find script in PROJECT_ROOT
        scriptpath = os.path.join(ST.PROJECT_ROOT, scriptpath)
        # copy submodule's images into sub_dir
        sub_dir = _sub_dir_name(scriptpath)
        sub_dirpath = os.path.join(cls.args.script, sub_dir)
        _copy_script(scriptpath, sub_dirpath)
        # read code
        pyfilename = os.path.basename(scriptpath).replace(cls.SCRIPTEXT, ".py")
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        with open(pyfilepath, 'r', encoding='utf8') as f:
            code = f.read()
        # replace tpl filepath with filepath in sub_dir
        code = re.sub(r"[\'\"](\w+.png)[\'\"]", r"\"%s/\g<1>\"" % sub_dir, code)
        exec(compile(code.encode("utf8"), pyfilepath, 'exec'), cls.scope)


def setup_by_args(args):
    # init devices
    if isinstance(args.device, list):
        devices = args.device
    elif args.device:
        devices = [args.device]
    else:
        devices = []
        print("do not connect device")

    # set base dir to find tpl
    dirpath, _ = script_dir_name(args.script)

    # set log dir
    if args.log:
        args.log = script_log_dir(dirpath, args.log)
        print("save log in '%s'" % args.log)
    else:
        print("do not save log")

    # set snapshot quality
    if args.compress:
        compress = args.compress
    else:
        compress = ST.SNAPSHOT_QUALITY

    if args.no_image:
        ST.SAVE_IMAGE = False

    # guess project_root to be basedir of current .air path
    project_root = os.path.dirname(args.script) if not ST.PROJECT_ROOT else None

    auto_setup(dirpath, devices, args.log, project_root, compress)


def run_script(parsed_args, testcase_cls=AirtestCase):
    global args  # make it global deliberately to be used in AirtestCase & test scripts
    args = parsed_args
    suite = unittest.TestSuite()
    suite.addTest(testcase_cls())
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    # if not result.wasSuccessful():
    #     sys.exit(-1)


def custom_resize_method(w, h, sch_resolution, src_resolution):
    """
    Resolution Adaptation Rules
    :param w:
    :param h:
    :param sch_resolution:
    :param src_resolution:
    :return: device resolution
    """
    return int(w), int(h)


def run_air(devices, case, app_name, log_path, case_path, base_dir,
            static_dir=decryption('aHR0cHM6Ly9mYXN0bHkuanNkZWxpdnIubmV0L2doL29wZW51dHgvc3RhdGljLw=='), record=None):
    """
    //See also: https://www.theiphonewiki.com/wiki/Models

    :param devices: read device id
    :param case: case list
    :param record: whether to enable recording
    :param log_path: log_path
    :param case_path: case_path
    :param base_dir: base_dir
    :param app_name: app_name
    :param static_dir: use local style file when empty

    :return:
    """

    connect_device(devices)

    if device_platform().lower() in 'ios':
        _device = ios_device_info()
        model = _device['MarketName']
        build_version = _device['ProductVersion']
        dev = model + ' ios {}'.format(build_version).replace('\n', '').replace('\r', '')

    elif device_platform().lower() in 'android':
        serialno = device().serialno
        model = ADB(serialno=serialno).get_model()
        build_version = shell('getprop ro.build.version.release')
        dev = model + ' Android {}'.format(build_version).replace('\n', '').replace('\r', '')
    else:
        print('{} is unsupported platform on utx!'.format(device_platform()))
        raise AirtestError('utx unsupported this platform!')

    UT.SYS = False
    UT.LOOP = 1
    popup(devices=devices)

    if os.path.isdir(log_path):
        pass
    else:
        os.makedirs(log_path)
        print(str(log_path) + 'is created')

    if str(case).endswith(".air"):
        if plat() == 'Windows':
            air_name = str(case).split('\\')[-1]
        else:
            air_name = str(case).split('/')[-1]

        if record:
            record = air_name.replace('.air', '.mp4')

        print(case)
        log = os.path.join(log_path + '/' + dev + '/' + air_name.replace('.air', ''))

        run_log = case + '/' + 'log' + '/' + dev
        if not os.path.exists(run_log):
            os.makedirs(run_log)
        print(log)
        if os.path.isdir(log):
            pass
        else:
            os.makedirs(log)
            print(str(log) + 'is created')
        output_file = log + '/' + 'log.html'
        args = Namespace(device=devices, log=run_log, recording=record, script=case, compress=20, no_image=False)
        try:
            run_script(args, AirtestCase)
        except (AirtestError, PocoException):
            pass
        finally:
            rpt = report.LogToHtml(case, run_log, script_name=air_name.replace(".air", ".py"), static_root=static_dir,
                                   plugins=['utx.mod.report.seleniumui', 'utx.mod.report.pocoui'])
            rpt.report("log_template.html", output_file=output_file, base_dir=base_dir)
            result = {"name": air_name.replace('.air', ''), "result": rpt.test_result}

        stop_app(app_name)
        time.sleep(2)
        start_app(app_name)
        time.sleep(2)

        return result, dev


def run_web_air(case, log_path, case_path, base_dir,
                static_dir=decryption('aHR0cHM6Ly9mYXN0bHkuanNkZWxpdnIubmV0L2doL29wZW51dHgvc3RhdGljLw==')):
    """

    :param case:
    :param log_path:
    :param case_path:
    :param base_dir:
    :param static_dir:
    :return:
    """
    dev = 'chrome'
    time.sleep(2)

    if os.path.isdir(log_path):
        pass
    else:
        os.makedirs(log_path)
        print(str(log_path) + 'is created')

    if str(case).endswith(".air"):
        if plat() == 'Windows':
            air_name = str(case).split('\\')[-1]
        else:
            air_name = str(case).split('/')[-1]
        print(case)
        log = os.path.join(log_path + '/' + dev + '/' + air_name.replace('.air', ''))

        run_log = case + '/' + 'log' + '/' + dev
        if not os.path.exists(run_log):
            os.makedirs(run_log)
        print(log)
        if os.path.isdir(log):
            pass
        else:
            os.makedirs(log)
            print(str(log) + 'is created')
        output_file = log + '/' + 'log.html'
        args = Namespace(device=None, log=run_log, recording=None, script=case, compress=20, no_image=False)
        try:
            run_script(args, AirtestCase)
        except Exception:
            pass
        finally:
            rpt = report.LogToHtml(case, run_log, script_name=air_name.replace(".air", ".py"), static_root=static_dir,
                                   plugins=['utx.mod.report.seleniumui', 'utx.mod.report.pocoui'])
            rpt.report("log_template.html", output_file=output_file, base_dir=base_dir)
            result = {"name": air_name.replace('.air', ''), "result": rpt.test_result}

        return result, dev
