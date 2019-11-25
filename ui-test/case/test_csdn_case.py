import time
import unittest

from page.csdn_page import CsdnPage


# csdn 流程用例测试
class TestCsdnCase(unittest.TestCase):
    # 放在各个测试方法中首行执行
    def before_setUp(self):
        print("一个测试点开始")
        # 创建 csdn 页面类并开启一个谷歌驱动
        self.csdn_page = CsdnPage()

    # 放在各个测试方法中末行执行
    def after_tearDown(self):
        print("一个测试点结束")
        # 关闭浏览器并退出驱动
        self.csdn_page.close()

    # 第一个测试点
    def test_1(self):
        print("这是第一个测试点")
        # 初始化
        self.before_setUp()

        # 开启 csdn 页面
        self.csdn_page.jump_to()
        # 休眠 5 秒方便看效果
        time.sleep(5)

        # 释放
        self.after_tearDown()


# 当前用例程序入口
if __name__ == "__main__":
    # 使用 unittest 依次执行当前模块中 test 打头的方法
    unittest.main()
