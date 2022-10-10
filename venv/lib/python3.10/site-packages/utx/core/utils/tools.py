#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  8/31/2021 9:42 PM
@Desc    :  Tools line.
"""
import base64
import platform
import socket
import subprocess
import re
import configparser
import requests
import urllib3
from multiprocessing import Process
from airtest.core.android.recorder import Recorder
from airtest.core.error import AdbShellError
from loguru import logger
from tqdm import tqdm
from airtest.utils.logger import get_logger
from airtest.core.api import *
from airtest.core.android.adb import ADB

LOGGING = get_logger(__name__)


def allure_report(report_path, report_html):
    """
    Generate allure Report
    :param report_path:
    :param report_html:
    :return:
    """
    # execution allure generate
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    try:
        subprocess.call(allure_cmd, shell=True)
    except Exception:
        LOGGING.error("The generation of allure report failed. Please check the relevant configuration of the test "
                      "environment")
        raise


def plat():
    """
    Check the current script running platform
    :return:'Linux', 'Windows' or 'Darwin'.
    """
    return platform.system()


def check_port(port):
    """
    Detect whether the port is occupied and clean up
    :param port:System port
    :return:None
    """
    if plat() != 'Windows':
        os.system("lsof -i:%s| grep LISTEN| awk '{print $2}'|xargs kill -9" % port)
    else:
        port_cmd = 'netstat -ano | findstr {}'.format(port)
        r = os.popen(port_cmd)
        if len(r.readlines()) == 0:
            return
        else:
            pid_list = []
            for line in r.readlines():
                line = line.strip()
                pid = re.findall(r'[1-9]\d*', line)
                pid_list.append(pid[-1])
            pid_set = list(set(pid_list))[0]
            pid_cmd = 'taskkill -PID {} -F'.format(pid_set)
            os.system(pid_cmd)


def cleanup():
    """
    cleanup device wda process
    :return:
    """
    pid_list = []
    cmd = decryption(b'dGlkZXZpY2U=')
    sub = subprocess.Popen(f'{cmd} ps', shell=True, close_fds=True, stdout=subprocess.PIPE)
    sub.wait()
    pid_info = sub.stdout.read().decode().splitlines()
    for u in pid_info:
        if 'WebDriverAgentRunner' in u:
            pid_list.append(u.strip().split(' ')[0])
    [os.system(f'{cmd} kill {pid}') for pid in pid_list]


def display():
    """
    Gets the length and width of the current device
    :return:
    """
    width, height = device().get_current_resolution()
    return width, height


def device_udid(state, types: str):
    """
    Perform `adb devices` command and return the list of adb devices
    Perform `utx list` command and return the list of iphone devices
    :param types: mobile platform
    :param state: optional parameter to filter devices in specific state
    :return: list od android devices or ios devices
    """
    device_list = []
    if types.lower() == 'android':
        patten = re.compile(r'^[\w\d.:-]+\t[\w]+$')
        output = ADB().cmd("devices", device=False)
        for line in output.splitlines():
            line = line.strip()
            if not line or not patten.match(line):
                continue
            serialno, cstate = line.split('\t')
            if state and cstate != state:
                continue
            device_list.append(serialno)
    elif types.lower() == 'ios':
        # Get the udid list of the connected mobile phone
        sub = subprocess.Popen('utx list', shell=True, close_fds=True, stdout=subprocess.PIPE)
        sub.wait()
        udid = sub.stdout.read().decode().splitlines()
        for u in udid:
            us = u.strip().split(' ')[0]
            if us != 'UDID':
                device_list.append(us)
    return device_list


def ios_device_info():
    """
    Gets device_info of the current device

    :return:
    """
    res = subprocess.run('{} info'.format(decryption(b'dGlkZXZpY2U=')), shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    lines = res.stdout.decode("utf-8", "ignore")
    device_info = [info for info in lines.split('\n') if info]
    _device = {}
    if len(device_info) < 2:
        LOGGING.error(f'Read device info line error. {lines}')
    for info in device_info:
        info_kv = info.split(':')
        if info_kv[0] == 'ProductVersion':
            _device['ProductVersion'] = info_kv[1].strip()
        if info_kv[0] == 'MarketName':
            _device['MarketName'] = info_kv[1].strip()
        if info_kv[0] == 'SerialNumber':
            _device['SerialNumber'] = info_kv[1].strip()
    return _device


def get_report(airtest_report_path):
    """
    Get the latest test report path
    :return: report name and path
    """
    file_lists = os.listdir(airtest_report_path)
    file_lists.sort(key=lambda fn: os.path.getmtime(airtest_report_path + "/" + fn)
    if not os.path.isdir(airtest_report_path + "/" + fn) else 0)
    report = os.path.join(airtest_report_path, file_lists[-1])
    print(file_lists[-1])
    return report


def encryption(value):
    """
    encryption
    https://cdn.jsdelivr.net/gh/openutx/static/
    :param value:
    :return:
    """
    bytes_url = value.encode("utf-8")
    str_url = base64.b64encode(bytes_url)
    return str_url


def decryption(value):
    """
    decryption
    https://cdn.jsdelivr.net/gh/openutx/static/
    :param value:
    :return:
    """
    str_url = base64.b64decode(value).decode("utf-8")
    return str_url


def str_to_bool(value):
    """
    str convert bool
    :param value:
    :return:
    """
    return True if value.lower() == 'true' else False


def find_all_cases(base, status, mark):
    """

    :param base:
    :param status:
    :param mark:
    :return:
    """
    for root, ds, fs in os.walk(base, topdown=True):
        if status in ["0", False]:
            for f in ds:
                if f.endswith('.air') and mark in f:
                    fullname = os.path.join(root, f)
                    yield fullname
        else:
            for f in ds:
                if f.endswith('.air'):
                    fullname = os.path.join(root, f)
                    yield fullname


def get_host_ip():
    """
    Query the local ip address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def proxy(devices, status=True):
    """
    android proxy
    :param devices:
    :param status: on or off
    :return:
    :platforms: Android
    """
    if status:
        proxy_cmd = f"{ADB.builtin_adb_path()} -s {devices} {decryption(b'c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5')} {get_host_ip()}:8888"
        logger.info(f'Successfully enabled {devices} global proxy！')
        os.system(proxy_cmd)
    else:
        proxy_cmd = f"{ADB.builtin_adb_path()} -s {devices} {decryption(b'c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5IDow')}"
        logger.info(f'Close the {devices} global proxy successfully！')
        os.system(proxy_cmd)


def selector(status, flag, cases_list):
    """

    :param status:
    :param flag:
    :param cases_list:
    :return:
    """
    cases = []
    if status in ["0", False]:
        for suite in cases_list:
            if flag in suite:
                if suite.endswith(".air"):
                    cases.append(suite)
    else:
        for suite in cases_list:
            if suite.endswith(".air"):
                cases.append(suite)

    return cases


def selector_v2(path, status, mark):
    cases = []
    for i in find_all_cases(path, status, mark):
        print(i)
        cases.append(i)
    return sorted(cases)


def selector_v3(path: str, status, mark):
    """

    :param path:
    :param status:
    :param mark:
    :return:
    """
    cases = []
    base_path = path.split(path.split('/')[-1])[0]
    path_list = ''.join(str(path).split()[0].split('/')[-1]).split(',')
    for item in path_list:
        for i in find_all_cases(base_path + item, status, mark):
            print(i)
            cases.append(i)
    return sorted(cases)


def download(file_url, types):
    """

    :param types:
    :param file_url:
    :return:
    """
    if 'http' not in file_url:
        return
    download_url = 'http' + file_url.split('http')[-1]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = requests.get(download_url, stream=True, verify=False)
    total = int(r.headers.get('content-length', 0))
    filename = "{}utx_download_{}.{}".format(file_url.split('http')[0], int(round(time.time() * 1000)), types)

    with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    return filename


def start_recording(max_time=1800):
    """

    :param max_time:
    :return:
    """
    serialno = device().serialno
    model = ADB(serialno=serialno)
    recorder = Recorder(model)
    recorder.start_recording(max_time=max_time)


def stop_recording(file, name=None):
    """

    :param file: __file__
    :param name: mp4 name
    :return: video file
    """
    serialno = device().serialno
    model = ADB(serialno=serialno)
    build_version = shell('getprop ro.build.version.release')
    dev = model.get_model() + ' Android {}'.format(build_version).replace('\n', '').replace('\r', '')
    recorder = Recorder(model)
    if not name:
        name = str(file).split('/')[-1].split('.')[0]
    output_path = os.path.join(str(file).split('.air')[0] + '.air', 'log', dev, name)
    recorder.stop_recording(output=f'{output_path}.mp4')


def check_network():
    """
    :return:
    """
    try:
        result = shell('ping -c 1 www.baidu.com')
        logger.info(result)
        return True
    except AdbShellError as e:
        logger.error(e)
        return False


def proxy_dump():
    """
    proxy filter url address
    :return:
    """

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"Created file: {path}"
        print(msg)

    content = """#!/usr/bin/python
# encoding=utf-8

\"\"\" Can only be modified by the administrator. Only proxy are provided.
\"\"\"

from garbevents.capture import GetData

addons = [
    GetData()
]
"""
    create_file(os.path.join("proxy.py"), content)
    try:
        from garbevents.cli.main import mitmweb
        from garbevents.settings import Settings as ST
        mitmweb(args=["-p", f"{ST.server_port}", "--ssl-insecure", "--web-host", f"{ST.web_host}", "--web-port",
                      f"{ST.web_port}", "--no-web-open-browser", "-s", "proxy.py"])
    except (ImportError, AttributeError):
        logger.error(
            "garbevents not installed, please run: pip install -U garbevents")
        return


def launcher(main, salve):
    """

    :param main:
    :param salve:
    :return:
    """
    master = Process(target=main)
    salver = Process(target=salve)
    salver.daemon = True
    master.daemon = True
    salver.start()
    master.start()
    master.join()


class ReadConfig:
    """
    configuration file
    """

    def __init__(self, ini_path):
        self.ini_path = ini_path
        if not os.path.exists(ini_path):
            raise FileNotFoundError("Profile %s does not exist！" % ini_path)
        self.config = configparser.RawConfigParser()  # When there are% symbols, use raw to read
        self.config.read(ini_path, encoding='utf-8')

    def _get(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """

        :param section:
        :param option:
        :param value:
        :return:
        """
        try:
            self.config.set(section, option, value)
        except configparser.NoSectionError as e:
            logger.error(e)
        with open(self.ini_path, 'w') as f:
            self.config.write(f)

    def getvalue(self, env, name):
        return self._get(env, name)

    def update_value(self, env, name, value):
        return self._set(env, name, value)
