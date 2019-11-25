import time
import unittest

from selenium import webdriver
from page.baidu_main_page import BaiduMainPage
from page.baidu_result_page import BaiduResultPage


# 百度页流程用例测试
class TestBaiduCase(unittest.TestCase):
    # @BeforeTest
    def setUp(self):
        print("一个测试点开始")
        # 开启一个谷歌驱动
        self.driver = webdriver.Chrome(
            "D:\\pythonproject\\python-ui-auto-test\\ui-test\\resource\\driver\\chromedriver.exe")

    # @AfterTest
    def tearDown(self):
        print("一个测试点结束")
        # 驱动退出
        self.driver.quit()

    # 第一个测试点
    def test_1(self):
        print("这是第一个测试点")
        # 初始化百度页面
        main_page = BaiduMainPage(self.driver)
        result_page = BaiduResultPage(self.driver)

        # 开启百度首页
        main_page.jump_to()
        # 首页搜索
        main_page.search()
        # 点击结果页的第一条链接
        result_page.click_first_link()
        # 休眠 5 秒方便看效果
        time.sleep(5)

    # 第二个测试点
    def test_2(self):
        print("这是第二个测试点")


# 当前用例程序入口
if __name__ == "__main__":
    # 使用 unittest 依次执行当前模块中 test 打头的方法
    unittest.main()
