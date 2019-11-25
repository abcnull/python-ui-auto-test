from common.page_common import PageCommon
from locator.baidu_result_locator import BaiduResultLocator


# 百度结果页页面类
class BaiduResultPage(PageCommon):
    # 百度搜索结果页点击第一行链接操作
    def click_first_link(self):
        self.click_element(BaiduResultLocator.link_a)
