import threading


# 本地线程存储器
class ThreadLocalStorage:
    # 类变量
    key_value = {}

    # 存储线程和对应线程的数据
    @classmethod
    def set(cls, thread, data):
        cls.key_value.update({thread: data})

    # 通过键名取值
    @classmethod
    def get(cls, thread):
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
