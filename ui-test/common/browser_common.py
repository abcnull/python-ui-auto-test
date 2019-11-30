import time


# 浏览器类封装浏览器操作
class BrowserCommon(object):
    # 初始化驱动相关
    def __init__(self, driver=None):
        """
        传驱动
        :param driver: 驱动
        """
        if driver:
            self.driver = driver
        else:
            raise RuntimeError("页面类初始化驱动必传！")
        # 设置 20 s 隐式等待
        self.driver.implicitly_wait(20)

    ############################## 获取浏览器属性 ##############################

    # 获取当前页面窗口句柄
    def get_window_handle(self):
        return self.driver.current_window_handle

    # 获取当前所有页面窗口句柄
    def get_window_handles(self):
        return self.driver.window_handles

    # 获取当前页面标题
    def get_title(self):
        return self.driver.title

    # 获取当前页面网址
    def get_url(self):
        return self.driver.current_url

    # 返回当前驱动
    def get_driver(self):
        return self.driver

    ############################## 浏览器切换操作 ##############################

    # 切换 frame
    def switch_to_frame(self, param):
        self.driver.switch_to.frame(param)

    # 切换alter
    def switch_to_alert(self):
        return self.driver.switch_to.alert

    # 切换窗口句柄
    def switch_to_window_handle(self, url=""):
        """
        切换窗口
            窗口数 == 1，提示只有个一个窗口
            窗口数 == 2，切换另一个窗口
            窗口数 >= 3，切换到指定窗口
        """
        # 获取当前所有句柄
        window_handles = self.get_window_handles()
        # 窗口数 == 1
        if len(window_handles) == 1:
            pass
        elif len(window_handles) == 2:
            # 获取另一个窗口句柄
            the_other_handle = window_handles[1 - window_handles.index(self.get_window_handle)]
            # 切换句柄
            self.driver.switch_to.window(the_other_handle)
        else:
            for handle in window_handles:
                # 切换句柄
                self.driver.switch_to.window(handle)
                # url 匹配到指定句柄时停止循环
                if url in self.get_url():
                    break

    ############################## 浏览器其他操作 ##############################

    # 驱动退出
    def close(self):
        self.driver.quit()
        # self.undeploy_all()

    # 休眠一定时间
    def sleep(self, seconds=2):
        time.sleep(seconds)

    # 执行 JS
    def execute_script(self, js, *args):
        self.driver.execute_script(js, *args)
