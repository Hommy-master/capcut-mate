import datetime
import random
import threading

class UniqueIDGenerator:
    _instance = None
    _lock = threading.Lock()  # 线程安全锁

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self._last_timestamp = ""
            self._counter = 0
            self.__initialized = True

    def generate(self) -> str:
        with self._lock:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            
            # 同一秒内：序列号+随机数组合防重
            if timestamp == self._last_timestamp:
                self._counter += 1
                serial = str(self._counter).zfill(3)  # 3位序列号（支持每秒1000次调用）
                random_part = str(random.randint(0, 999)).zfill(3)  # 3位随机数
                return timestamp + serial + random_part
            else:
                self._last_timestamp = timestamp
                self._counter = 0
                return timestamp + str(random.randint(0, 999999)).zfill(6)
