import logging.config
import os
from util.config_reader import ConfigReader

# 用户名字典
dic = {
    # 用户名
    'username': 'abcnull'
}

# 定义三种日志输出格式
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 从配置文件取到的日志配置信息
# 输出日志的名字和绝对路径
logfile_name = ConfigReader().read('log')['logfile_name']  # log文件名
logfile_path_staff = r'' + os.path.abspath(os.path.dirname(__file__))[
                           :os.path.abspath(os.path.dirname(__file__)).find("python-ui-auto-test\\") + len(
                               "python-ui-auto-test\\")] + "ui-test" + ConfigReader().read('log')[
                         'logfile_path'] + logfile_name

# 打到终端的日志级别和格式
terminal_level = ConfigReader().read('log')['terminal_level']
terminal_formatter = ConfigReader().read('log')['terminal_formatter']
# 打到文件的日志级别和格式
file_level = ConfigReader().read('log')['file_level']
file_formatter = ConfigReader().read('log')['file_formatter']
# 既打到终端又打到文件的日志级别
all_level = ConfigReader().read('log')['all_level']
# 日志文件存储字节数
max_bytes = int(ConfigReader().read('log')['max_bytes'])
# 日志文件轮转数
backup_count = int(ConfigReader().read('log')['backup_count'])
# 日志文件编码方式
encoding = ConfigReader().read('log')['encoding']

# log 配置字典
# logging_dic 第一层的所有的键不能改变
logging_dic = {
    # 版本号
    'version': 1,
    # 固定写法
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'sh': {
            'level': terminal_level,
            # 打印到屏幕
            'class': 'logging.StreamHandler',
            'formatter': terminal_formatter
        },
        # 打印到文件的日志,收集info及以上的日志
        'fh': {
            'level': file_level,
            # 保存到文件
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': file_formatter,
            # 日志文件
            'filename': logfile_path_staff,
            # 日志大小 300字节
            'maxBytes': max_bytes,
            # 轮转文件的个数
            'backupCount': backup_count,
            # 日志文件的编码
            'encoding': encoding,
        },
    },
    'loggers': {
        # logging.getLogger(__name__) 拿到的 logger 配置
        '': {
            # 这里把上面定义的两个handler都加上，即 log 数据既写入文件又打印到屏幕
            'handlers': ['sh', 'fh'],
            'level': all_level,
            # 向上（更高 level 的 logger）传递
            'propagate': True,
        },
    },
}


# log 日志工具（已对其进行了封装）
def log():
    # 导入上面定义的 logging 配置 通过字典方式去配置这个日志
    logging.config.dictConfig(logging_dic)
    # 生成一个 log 实例，这里可以有参数传给 task_id
    logger = logging.getLogger()
    return logger


# 用例开始
def start_info():
    log().info(f"<测试开始>")


# 用例结束
def end_info():
    log().info(f"<测试结束>")


# 用例登陆成功
def login_info():
    log().info(f"{dic['username']} 登陆成功")

# 尝试（单独测试这里可以取消注释，之后这里请务必要注释掉！）
# login_info()
# start_info()
# end_info()
