import time
import unittest
from BeautifulReport import BeautifulReport
from base.assembler import Assembler
from page.csdn_page import CsdnPage
from util.log_tool import start_info, end_info, log
from util.screenshot_tool import ScreenshotTool


# 其他流程用例测试
class TestOtherCase(unittest.TestCase):
    # 出错需要截图时此方法自动被调用
    def save_img(self, img_name):
        ScreenshotTool().save_img(self.driver, img_name)

    # @BeforeTest
    def setUp(self):
        # 开始的 log 信息
        start_info()
        # 装配器初始化并开启一个谷歌驱动
        self.assembler = Assembler()
        self.driver = self.assembler.get_driver()

    # @AfterTest
    def tearDown(self):
        # 结束的 log 信息
        end_info()
        # 装配器卸载
        self.assembler.disassemble_all()

    # 第一个测试点
    @BeautifulReport.add_test_img(ScreenshotTool().get_img_name("../report/img/test_1_TestOtherCase"))
    def test_1_TestOtherCase(self):
        # log 信息
        log().info(f"其他测试第一个用例")

        # 创建 csdn 页面类
        csdn_page = CsdnPage(self.driver)
        # 开启 csdn 页面
        csdn_page.jump_to()
        # 休眠 2 秒方便观察页面运行效果
        time.sleep(2)

        # 手动断言错误
        assert False
