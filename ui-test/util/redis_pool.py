#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : abcnull
# @Time : 2019/12/2 17:37
# @E-Mail : abcnull@qq.com
# @CSDN : abcnull
# @GitHub : abcnull

import redis as redis
from util.config_reader import ConfigReader


# redis 连接池工具
class RedisPool:
    # 初始化连接池并直接创建一个 redis 连接
    def __init__(self):
        # redis_ip
        self.host = ConfigReader().read("redis")["redis_ip"]
        # redis_port
        self.port = int(ConfigReader().read("redis")["redis_port"])
        # redis_pwd
        self.password = ConfigReader().read("redis")["redis_pwd"]
        # 最大连接数
        self.max_connections = int(ConfigReader().read("redis")["max_connections"])
        # redis 连接池
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password,
                                         max_connections=self.max_connections)
        # redis 的一个连接
        self.conn = redis.Redis(connection_pool=self.pool)

    # 获取 redis 连接池
    def get_redis_pool(self):
        return self.pool

    # 获取 redis 连接
    def get_redis_conn(self):
        return self.conn

    # 获取 redis 的一个新的连接池
    def get_new_redis_pool(self):
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password,
                                         max_connections=self.max_connections)
        self.conn = redis.Redis(connection_pool=self.pool)
        return self.pool

    # 获取 redis 的一个新的连接
    def get_new_redis_conn(self):
        self.conn = redis.Redis(connection_pool=self.pool)
        return self.conn

    # 关闭当前的连接
    def release_redis_conn(self):
        if self.conn is not None:
            self.conn.connection_pool.disconnect()
            self.conn = None

    # 关闭整个连接池
    def release_redis_pool(self):
        if self.pool is not None:
            self.pool.disconnect()
            self.pool = None
