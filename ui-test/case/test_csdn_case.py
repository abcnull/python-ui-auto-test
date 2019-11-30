import time
import unittest
from BeautifulReport import BeautifulReport
from base.assembler import Assembler
from page.csdn_page import CsdnPage
from util.log_tool import start_info, end_info, log
from util.screenshot_tool import ScreenshotTool


# csdn 流程用例测试
class TestCsdnCase(unittest.TestCase):
    # 出错需要截图时此方法自动被调用
    def save_img(self, img_name):
        ScreenshotTool().save_img(self.driver, img_name)

    # 放在各个测试方法中首行执行
    def before_setUp(self):
        # 开始的 log 信息
        start_info()
        # 装配器初始化并开启一个谷歌驱动
        self.assembler = Assembler()
        self.driver = self.assembler.get_driver()
        # 创建 csdn 页面类
        self.csdn_page = CsdnPage(self.driver)

    # 放在各个测试方法中末行执行
    def after_tearDown(self):
        # 结束的 log 信息
        end_info()
        # 装配器卸载
        self.assembler.disassemble_all()

    # 第一个测试点
    @BeautifulReport.add_test_img(ScreenshotTool().get_img_name("../report/img/test_1_TestCsdnCase"))
    def test_1_TestCsdnCase(self):
        # 初始化
        self.before_setUp()

        # log 信息
        log().info(f"csdn 测试第一个用例")

        # 开启 csdn 页面
        self.csdn_page.jump_to()
        # 休眠 2 秒方便看效果
        time.sleep(2)

        # 强行截图
        ScreenshotTool().save_img(self.driver, "force_test_1_TestCsdnCase")

        # 释放
        self.after_tearDown()


# 当前用例程序入口
if __name__ == "__main__":
    # 使用 unittest 依次执行当前模块中 test 打头的方法
    unittest.main()
