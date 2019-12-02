#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : abcnull
# @Time : 2019/12/2 17:37
# @E-Mail : abcnull@qq.com
# @CSDN : abcnull
# @GitHub : abcnull

import threading


# 本地线程存储器
class ThreadLocalStorage:
    # 类变量
    key_value = {}

    # 存储线程和对应线程的数据
    @classmethod
    def set(cls, thread, data):
        """
        类变量字典保存 {线程: 数据} 的键值对
        :param thread: 当前线程
        :param data: 需要保存的数据
        """
        cls.key_value.update({thread: data})

    # 通过键名取值
    @classmethod
    def get(cls, thread):
        """
        得到线程对应的存储数据
        :param thread: 线程
        :return: 返回对应线程的数据
        """
        return cls.key_value[thread]

    # 清空当前线程存储的对应数据
    @classmethod
    def clear_current_thread(cls):
        del cls.key_value[threading.current_thread()]

    # 清空所有线程以及所有线程存储的对应数据
    @classmethod
    def clear_all_thread(cls):
        cls.key_value.clear()
        cls.key_value = {}
