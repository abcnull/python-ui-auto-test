from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from common.browser_common import BrowserCommon


# Page 项目无关页面类
class PageCommon(BrowserCommon):
    # 获取当前页面窗口句柄
    @property
    def get_window_handle(self):
        return self.driver.current_window_handle

    # 获取当前页面标题
    @property
    def get_title(self):
        return self.driver.title

    # 获取当前页面网址
    @property
    def get_url(self):
        return self.driver.current_url

    ############################## 基本元素操作 ##############################

    # 点击元素
    def click_element(self, xpath):
        # 显示等待元素可点击
        WebDriverWait(self.driver, 10, 0.1).until(expected_conditions.element_to_be_clickable(("xpath", xpath)))
        # 点击元素
        self.driver.find_element_by_xpath(xpath).click()

    # 输入框输入数据
    def input(self, xpath, value):
        # 显示等待元素可点击
        WebDriverWait(self.driver, 10, 0.1).until(expected_conditions.element_to_be_clickable(("xpath", xpath)))
        # 输入框输入数据
        self.driver.find_element_by_xpath(xpath).send_keys(value)
