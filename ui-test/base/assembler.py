#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : abcnull
# @Time : 2019/12/2 17:37
# @E-Mail : abcnull@qq.com
# @CSDN : abcnull
# @GitHub : abcnull

import os
import threading
from selenium import webdriver
from util.config_reader import ConfigReader
from util.mysql_tool import MysqlTool
from util.redis_pool import RedisPool
from util.thread_local_storage import ThreadLocalStorage
from selenium.webdriver.chrome.webdriver import RemoteWebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions


# 初始装配工具（一个线程分配一个驱动，一个 redis 连接，一个 mysql 连接）
class Assembler:
    # 初始化所有工具
    def __init__(self):
        # 驱动装配
        self.assemble_driver()
        # redis 工具装配
        if ConfigReader().read("project")["redis_enable"].upper() == "Y":
            # 装配 redis 连接池工具
            self.assemble_redis()
        elif ConfigReader().read("project")["redis_enable"].upper() == "N":
            self.redis_pool_tool = None
        else:
            self.redis_pool_tool = None
            raise RuntimeError("配置文件中配置 redis 是否启用字段有误！请修改！")
        # mysql 工具装配
        if ConfigReader().read("project")["mysql_enable"].upper() == "Y":
            # 装配 mysql 工具
            self.assemble_mysql()
        elif ConfigReader().read("project")["mysql_enable"].upper() == "N":
            self.mysql_tool = None
        else:
            self.mysql_tool = None
            raise RuntimeError("配置文件中配置 mysql 是否启用字段有误！请修改！")
        # 将装配器保存到线程存储器中，键名为线程，键值为装配器对象
        ThreadLocalStorage.set(threading.current_thread(), self)

    # 卸下所有
    def disassemble_all(self):
        # 卸下驱动
        self.disassemble_driver()
        # 卸下 redis 连接池工具
        self.disassemble_redis()
        # 卸下 mysql 工具
        self.disassemble_mysql()
        # 删除当前线程存储的 {当前线程: 装配器} 键值对
        ThreadLocalStorage.clear_current_thread()

    ############################## 驱动 ##############################
    # 装配驱动
    def assemble_driver(self):
        # 若是谷歌驱动
        if ConfigReader().read("project")["driver"].lower() == "chrome":
            # chrome option
            chrome_options = ChromeOptions()
            # 服务端 root 用户不能直接运行 chrome，添加此参数可以运行
            chrome_options.add_argument('--no-sandbox')
            # # 下面参数可自行选择
            # chrome_options.add_argument('--user-data-dir')
            # chrome_options.add_argument('--dns-prefetch-disable')
            # chrome_options.add_argument('--lang=en-US')
            # chrome_options.add_argument('--disable-setuid-sandbox')
            # chrome_options.add_argument('--disable-gpu')

            # 驱动路径
            executable_path = os.path.abspath(os.path.dirname(__file__))[
                              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("driver")[
                                  "chrome_driver_path"]
            # 如果读取不到 remote_ip 或者 remote_port 就不用远端浏览器
            if ConfigReader().read("project")["remote_ip"] == "" or ConfigReader().read("project")["remote_port"] == "":
                self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
            # 使用远端浏览器
            else:
                url = "http://" + ConfigReader().read("project")["remote_ip"] + ":" + ConfigReader().read("project")[
                    "remote_port"] + "/wd/hub"
                self.driver = RemoteWebDriver(command_executor=url, options=chrome_options)

        # 若是火狐驱动
        elif ConfigReader().read("project")["driver"].lower() == "firefox":
            # firefox option
            firefox_options = FirefoxOptions()
            # 服务端 root 用户不能直接运行 chrome，添加此参数可以运行
            firefox_options.add_argument('--no-sandbox')
            # 驱动路径
            executable_path = os.path.abspath(os.path.dirname(__file__))[
                              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("driver")[
                                  "firefox_driver_path"]
            # 获取驱动自己产出日志路径
            log_path = os.path.abspath(os.path.dirname(__file__))[
                       :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                           "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("log")["logfile_path"]
            self.driver = webdriver.Firefox(executable_path=executable_path, log_path=log_path + "geckodriver.log",
                                            firefox_options=firefox_options)

        # 若是 IE 驱动
        elif ConfigReader().read("project")["driver"].lower() == "ie":
            # ie option
            ie_options = IeOptions()
            # 服务端 root 用户不能直接运行 chrome，添加此参数可以运行
            ie_options.add_argument('--no-sandbox')
            # 驱动路径
            executable_path = os.path.abspath(os.path.dirname(__file__))[
                              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("driver")["ie_driver_path"]
            self.driver = webdriver.Ie(executable_path=executable_path, ie_options=ie_options)

        # 若是 Edge 驱动
        elif ConfigReader().read("project")["driver"].lower() == "edge":
            executable_path = os.path.abspath(os.path.dirname(__file__))[
                              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("driver")[
                                  "edge_driver_path"]
            self.driver = webdriver.Edge(executable_path=executable_path)

        # 若是欧朋驱动
        elif ConfigReader().read("project")["driver"].lower() == "opera":
            executable_path = os.path.abspath(os.path.dirname(__file__))[
                              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("driver")[
                                  "opera_driver_path"]
            self.driver = webdriver.Opera(executable_path=executable_path)

        # 若是 Safari 驱动
        elif ConfigReader().read("project")["driver"].lower() == "safari":
            executable_path = os.path.abspath(os.path.dirname(__file__))[
                              :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test") + len(
                                  "python-ui-auto-test")] + "/ui-test" + ConfigReader().read("driver")[
                                  "safari_driver_path"]
            self.driver = webdriver.Safari(executable_path=executable_path)

        # 不支持的浏览器类型
        else:
            self.driver = None
            raise RuntimeError("配置文件中配置了不支持的浏览器类型！请修改浏览器类型！")

    # 卸下驱动
    def disassemble_driver(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    # 获取驱动
    def get_driver(self):
        return self.driver

    ############################## redis ##############################
    # 装配 redis 工具
    def assemble_redis(self):
        # redis 连接池工具
        self.redis_pool_tool = RedisPool()

    # 卸下 redis 工具
    def disassemble_redis(self):
        if self.redis_pool_tool is not None:
            # 关闭连接
            self.redis_pool_tool.release_redis_conn()
            # 关闭连接池
            self.redis_pool_tool.release_redis_pool()
            self.redis_pool_tool = None

    # 获取 redis 工具
    def get_redis(self):
        return self.redis_pool_tool

    ############################## mysql ##############################
    # 装配 mysql 工具
    def assemble_mysql(self):
        # mysql 连接
        self.mysql_tool = MysqlTool()

    # 卸下 mysql 工具
    def disassemble_mysql(self):
        if self.mysql_tool is not None:
            # 关闭 mysql 连接
            self.mysql_tool.release_mysql_conn()
            self.mysql_tool = None

    # 获取 mysql 工具
    def get_mysql(self):
        return self.mysql_tool
