# UTX
![PyPI](https://img.shields.io/pypi/v/utx) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utx) [![Downloads](https://static.pepy.tech/personalized-badge/utx?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=downloads/total)](https://pepy.tech/project/utx) ![GitHub top language](https://img.shields.io/github/languages/top/openutx/utx) ![GitHub stars](https://img.shields.io/github/stars/openutx/utx?style=social) ![https://blog.csdn.net/flower_drop](https://img.shields.io/badge/csdn-%40flower__drop-orange)
## logo
![](https://cdn.jsdelivr.net/gh/openutx/static/image/utx.png)
## 安装
- 命令行执行
```
pip install -U utx
```


## 设计理念

很大程度上借鉴了HttpRunner（优秀的框架）。不同的是，utx更着重写python，而不是写yaml文件。

- 简单是更好的
- 每个人都能用python写自动化
- UI自动化跟的上冲刺迭代和UI变更


这就是utx的设计理念。


## 项目结构
![](https://cdn.jsdelivr.net/gh/openutx/static/image/jg.png)

- utx提供了快速创建项目的能力，也就是脚手架。
- 【app脚手架】
```shell
utx startproject project_name
```
- 【web脚手架】
```shell
utx startproject-web project_name
```
```text
$ utx startproject demo
2021-09-01 12:39:16.491 | INFO     | utx.cli.scaffold:create_scaffold:51 - Create new project: demo
Project root dir: /PycharmProjects/demo

Created folder: demo
Created folder: demo/config
Created folder: demo/logs
Created folder: demo/packages
Created folder: demo/report/airtest
Created folder: demo/tests
Created folder: demo/suites
Created file: demo/.gitignore
Created file: demo/conftest.py
Created file: demo/pytest.ini
Created file: demo/run.py
Created file: demo/requirements.txt
Created file: demo/config/conf.py
Created file: demo/config/config.ini
Created file: demo/config/__init__.py
Created file: demo/tests/test_devices.py
Created file: demo/tests/__init__.py
Created file: demo/report/summary_template.html

```
## 调用流程图

![](https://cdn.jsdelivr.net/gh/openutx/static/image/lc.png)

## 专注于写脚本

- 项目结构很清晰。在conftest.py进行一些初始化/参数化/清理工作，在suites/写测试脚本。
>在AirtestIDE中写好.air脚本，然后将文件放到suites文件中。
- 更注重平铺写脚本的方式，这样就离“每个人都能用python写自动化”更近一步。毕竟封装之后看着容易晕，我也晕。
- 去除掉框架的约束，给每个人写python的自由，在测试脚本里你可以尽情发挥你的代码风格，代码能力，千人千面。代价呢，就是代码质量参差不齐。

大胆写，能写，写出来，跑通，就已经是在写自动化，就已经是在创造价值了！


## 轻封装

utx尊重原生用法。

airtest的封装只通过装饰器进行了运行方式的调整，没有做任何其他的冗余修改。

- faker，造数据工具
- pytest，测试框架
- airtest，自动化测试工具
- tidevice，iOS设备管理工具
- pandas、numpy，数据处理工具

安装utx，自动就把这些开源利器安装上了，无需单独安装。未来会集成更多实用工具到utx中。

utx本身是很轻的。

## 核心价值

- 上手 0 门槛，iOS/Android 设备均实现即插即用，随写随调
- 测试用例可读性高，编写成本低，支持python语法，便于公共操作抽象，进一步提高用例可维护性
- 用例执行高鲁棒性，多设备机型切换无需更改用例适配
- 执行集创建简单，支持智能并发、分组单模块执行，更高效更灵活

## 功能介绍

1. 支持android,ios,web 平台的自动化测试框架
2. 脚本批量执行
3. 每个脚本执行日志分开存放
4. 每个脚本单独生成一个html报告并在父文件夹生成一个聚合报告
5. 自定义的聚合报告，详细展示运行结果
6. 重试机制，运行失败自动重跑，可自定义重跑次数
7. 自定义脚本运行，可选择部分模块单独运行
8. 自带脚手架工具可以快速生成框架目录


## app使用说明

- 只需在配置文件中填好相关内容，即可运行！
```ini
[device_info]
;设备远程链接URL 设备ip+端口或者设备唯一标识id，多个设备以,分割；例如 设备1,设备2,设备3
device = 127.0.0.1:5555
;设备平台iOS或者Android
platform = android
;ios设备驱动包名，仅测试iOS时需要
wda = com.facebook.WebDriverAgentRunner.utx.xctrunner
;是否执行安装卸载操作 True/False
init = False

[app_info]
;app包名
package = com.wx.mp.test
;apk或者ipa文件名
filename = app_test.apk

[reruns]
;失败后再次运行次数，默认1次
times = 1

[paths]
;自定义执行case目录层级，文件夹名称（例如：smoke），默认为空
name = 

[mode]
;False 表示 运行[suites][cases]选择的用例，True表示运行全部用例
is_all = True
;是否录制视频 True/False
record = False

[suites]
;填写用例的关键字
cases = test.air
```

- app启动命令
1. 普通启动
```shell
python run.py
```
2. 参数化启动
```shell
# Android
python run.py --platform=Android --device=127.0.0.1:5555 --init=True
# iOS
python run.py --platform=iOS --wda=com.facebook.WebDriverAgentRunner.utx.xctrunner --init=True
```
>参数优先级大于配置文件
> >多个设备以,分割; 例如 python run.py --platform=Android --device=设备1,设备2,设备3 --init=True

## web使用说明

- 无需关注 chrome浏览器驱动
> 注意：无需配置 chromedriver ，系统会自动化维护匹配版本。
- 只需在配置文件中填好相关内容，即可运行！
```ini
[web_info]
;被测的主页url
url = https://www.baidu.com/
;是否无界面运行
headless = False

[reruns]
;失败后再次运行次数，默认1次
times = 1

[paths]
;自定义执行case目录层级，文件夹名称（例如：smoke），默认为空
name = 

[mode]
;False 表示 运行[suites][cases]选择的用例，True表示运行全部用例
is_all = True

[suites]
;填写用例的关键字
cases = chrome

```

- web启动命令
1. 普通启动
```shell
python run.py
```
2. 参数化启动
```shell
python run.py --headless=True --driver=/Users/admin/driverpath
```
>参数优先级大于配置文件

## 运行结果
- 报告展示

![](https://cdn.jsdelivr.net/gh/openutx/static/image/bg.png)

