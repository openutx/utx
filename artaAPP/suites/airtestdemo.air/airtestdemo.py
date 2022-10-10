# -*- encoding=utf8 -*-
__author__ = "manlokfaicharlie"

from airtest.core.api import *

# from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

# stop_app("com.k11.membership")

# start_app("com.arta.artazine.uat")

touch(Template(r"tpl1665138699549.png", record_pos=(-0.421, -0.965), resolution=(1080, 2400)))
assert_exists(Template(r"tpl1665138740937.png", record_pos=(-0.378, -0.776), resolution=(1080, 2400)), "Please fill in the test point.")
assert_not_exists(Template(r"tpl1665138699549.png", record_pos=(-0.421, -0.965), resolution=(1080, 2400)), "hi")


