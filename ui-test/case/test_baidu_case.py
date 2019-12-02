import time
import unittest
import paramunittest
from BeautifulReport import BeautifulReport
from base.assembler import Assembler
from data.csdn_data import CsdnData
from page.baidu_main_page import BaiduMainPage
from page.baidu_result_page import BaiduResultPage
from util.config_reader import ConfigReader
from util.log_tool import start_info, end_info, log
from util.screenshot_tool import ScreenshotTool


# 参数化构建参数
@paramunittest.parametrized(
    # 参数{语言，环境}
    {"lan": ConfigReader().read("project")["lan"], "env": ConfigReader().read("project")["env"]}
)
# 百度页流程用例测试
class TestBaiduCase(unittest.TestCase):
    # 出错需要截图时此方法自动被调用
    def save_img(self, img_name):
        ScreenshotTool().save_img(self.driver, img_name)

    # 参数化构建方法
    def setParameters(self, lan, env):
        self.lan = lan
        self.env = env

    # @BeforeTest
    def setUp(self):
        # 开始的 log 信息
        start_info()
        # 装配器初始化
        self.assembler = Assembler()

        # 提取驱动
        self.driver = self.assembler.get_driver()

        # 提取 redis 连接池工具
        self.redis_tool = self.assembler.get_redis()
        # 从连接池工具中拿到一个连接
        self.redis_conn = self.redis_tool.get_redis_conn()

        # # 提取 mysql 工具
        # self.mysql_tool = self.assembler.get_mysql()
        # # 从 mysql 工具中拿到一个连接
        # self.mysql_conn = self.mysql_conn.get_mysql_conn()

    # @AfterTest
    def tearDown(self):
        # 结束的 log 信息
        end_info()
        # 装配器卸载
        self.assembler.disassemble_all()

    # 第一个测试点
    @BeautifulReport.add_test_img(ScreenshotTool().get_img_name("../../report/img/test_1_TestBaiduCase"))
    def test_1_TestBaiduCase(self):
        # log 信息
        log().info(f"百度测试第一个用例，环境" + self.env + "语言" + self.lan)
        # 初始化百度页面
        main_page = BaiduMainPage(self.driver)
        result_page = BaiduResultPage(self.driver)

        # 开启百度首页
        main_page.jump_to()
        # 首页搜索
        main_page.search()
        # 点击结果页的第一条链接
        result_page.click_first_link()

        # redis 存储一条数据
        self.redis_conn.set("param", "百度")

        # 切换窗口句柄
        result_page.switch_to_window_handle(CsdnData.handle_url)
        # 休眠 2 秒方便观察页面运行效果
        time.sleep(2)

    # 第二个测试点
    @BeautifulReport.add_test_img(ScreenshotTool().get_img_name("../../report/img/test_1_TestBaiduCase"))
    def test_2_TestBaiduCase(self):
        # log 信息
        log().info(f"百度测试第二个用例，环境" + self.env + "语言" + self.lan)

        # 从 redis 取出数据
        log().info(f"从 redis 中取出数据：" + self.redis_conn.get("param").decode())

        # 休眠 2 秒方便观察页面运行效果
        time.sleep(2)


# 当前用例程序入口
if __name__ == "__main__":
    # 使用 unittest 依次执行当前模块中 test 打头的方法
    # verbosity=0 静默模式，仅仅获取总的测试用例数以及总的结果
    # verbosity=1 默认模式，在每个成功的用例前面有个’.’,每个失败的用例前面有个’F’
    # verbosity=2 详细模式，测试结果会显示每个测试用例的所有相关信息
    unittest.main(verbosity=0)
