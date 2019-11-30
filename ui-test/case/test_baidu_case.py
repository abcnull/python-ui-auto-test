import time
import unittest
from BeautifulReport import BeautifulReport
from base.assembler import Assembler
from data.csdn_data import CsdnData
from page.baidu_main_page import BaiduMainPage
from page.baidu_result_page import BaiduResultPage
from util.log_tool import start_info, end_info, log
from util.screenshot_tool import ScreenshotTool


# 百度页流程用例测试
class TestBaiduCase(unittest.TestCase):
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
    @BeautifulReport.add_test_img(ScreenshotTool().get_img_name("../report/img/test_1_TestBaiduCase"))
    def test_1_TestBaiduCase(self):
        # log 信息
        log().info(f"百度测试第一个用例")
        # 初始化百度页面
        main_page = BaiduMainPage(self.driver)
        result_page = BaiduResultPage(self.driver)

        # 开启百度首页
        main_page.jump_to()
        # 首页搜索
        main_page.search()
        # 点击结果页的第一条链接
        result_page.click_first_link()
        # 切换窗口句柄
        result_page.switch_to_window_handle(CsdnData.handle_url)
        # 休眠 2 秒方便观察页面运行效果
        time.sleep(2)

    # 第二个测试点
    @BeautifulReport.add_test_img(ScreenshotTool().get_img_name("../report/img/test_1_TestBaiduCase"))
    def test_2_TestBaiduCase(self):
        # log 信息
        log().info(f"百度测试第二个用例")
        # 休眠 2 秒方便观察页面运行效果
        time.sleep(2)


# 当前用例程序入口
if __name__ == "__main__":
    # 使用 unittest 依次执行当前模块中 test 打头的方法
    unittest.main()
