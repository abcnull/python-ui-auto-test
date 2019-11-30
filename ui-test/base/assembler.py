import os
import threading
from selenium import webdriver
from util.config_reader import ConfigReader
from util.thread_local_storage import ThreadLocalStorage


# 初始装配工具（做到一个线程一个驱动）
class Assembler:
    # 初始化所有工具
    def __init__(self):
        # 装配驱动
        self.assemble_driver()
        # 装配 redis
        self.assemble_redis()
        # 将装配器保存到线程存储器中，键名为线程，键值为装配器对象
        ThreadLocalStorage.set(threading.current_thread(), self)

    # 装配所有
    def disassemble_all(self):
        # 卸下驱动
        self.disassemble_driver()
        # 卸下 redis
        self.disassemble_redis()
        # 删除当前线程存储的 {当前线程: 装配器} 键值对
        ThreadLocalStorage.clear_current_thread()

    # 装配驱动
    def assemble_driver(self):
        self.driver = webdriver.Chrome(os.path.abspath(os.path.dirname(__file__))[
                                       :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test\\") + len(
                                           "python-ui-auto-test\\")] + "ui-test" + ConfigReader().read("driver_path")[
                                           "chrome_driver_path"])

    # 卸下驱动
    def disassemble_driver(self):
        self.driver.quit()

    # 获取驱动
    def get_driver(self):
        return self.driver

    # 装配 redis
    def assemble_redis(self):
        print("装配 redis")

    # 卸下 redis
    def disassemble_redis(self):
        print("卸下 redis")
