import logging
import os
from datetime import datetime
from config import read_config
import threading


class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = read_config.parDir
        resultPath = os.path.join(proDir, "result")
        # 日志文件不存在时，创建日志文件
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        # 按照用例执行时间命名文件名
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        # 测试日志不存在时创建
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # 定义日志
        self.logger = logging.getLogger()
        # 定义日志等级
        self.logger.setLevel(logging.INFO)

        # 创建文件处理器
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # 设置处理器格式
        handler.setFormatter(formatter)
        # 添加处理器到日志记录器
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            with MyLog.mutex:
                if MyLog.log is None:
                    MyLog.log = Log()

        return MyLog.log