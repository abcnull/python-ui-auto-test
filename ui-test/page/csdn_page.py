from common.page_common import PageCommon
from data.csdn_data import CsdnData


# csdn 页面类
class CsdnPage(PageCommon):
    # csdn 进入页面操作
    def jump_to(self):
        self.driver.get(CsdnData.url)
