from common.page_common import PageCommon
from data.baidu_main_data import BaiduMainData
from locator.baidu_main_locator import BaiduMainLocator


# 百度首页页面类
class BaiduMainPage(PageCommon):
    # 百度首页进入页面操作
    def jump_to(self):
        self.driver.get(BaiduMainData.url)

    # 搜索数据
    def search(self):
        self.input(BaiduMainLocator.search_input, BaiduMainData.data)
        self.click_element(BaiduMainLocator.search_btn)
