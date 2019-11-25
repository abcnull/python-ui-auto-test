import time

from selenium import webdriver


# 浏览器类
class BrowserCommon(object):
    # 初始化驱动相关
    def __init__(self, driver=None):
        if driver:
            self.driver = driver
        else:
            # 生成驱动
            self.driver = webdriver.Chrome(
                "D:\\pythonproject\\python-ui-auto-test\\ui-test\\resource\\driver\\chromedriver.exe")
            # 设置 20 s 隐式等待
            self.driver.implicitly_wait(20)

    # 返回当前驱动
    def get_driver(self):
        return self.driver

    # 驱动退出
    def close(self):
        self.driver.quit()

    # 休眠一定时间
    def sleep(self, seconds=2):
        time.sleep(seconds)
