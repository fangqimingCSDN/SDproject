"""
logger system
"""
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

def make_8lab_django_logger():
    """
    A logger using the django framework is typically configured in settings.py
    :return: logger
    """
    return logging.getLogger("app_views")

def instance_(func):
    """这么做还是不错的， 装饰器实现单例模式"""
    instance = {}
    def outwrapper(*args, **kwargs):
        print(instance)
        if func not in instance:
            instance[func] = func(*args, **kwargs)
        return instance[func]
    return outwrapper

@instance_
def make_8lab_django_logger2():
    # 编程的方式来写一下高级的写法# 记录器
    logger = logging.getLogger('sdproject')
    logger.setLevel(logging.INFO)
    # 处理器handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    # 没有给handler指定日志级别，将使用Logger的级别
    # fileHandler = logging.FileHandler(filename='sdproject.log')
    fileHandler = TimedRotatingFileHandler(filename="sdproject.log", when="midnight", interval=1, backupCount=2)
    # formatter格式
    FMT = '%(asctime)s %(filename)-6s [line:%(lineno)-2d] %(levelname)s: %(message)s'
    DATEFMT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=FMT, datefmt=DATEFMT)
#     formatter = logging.Formatter("%(asctime)s%(levelname)sl%(filename)s:%(lineno)sl%(message)s")
    # 给处理器设置格式consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    # 记录器要设置处理器
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
    return logger


logger = make_8lab_django_logger2()
# logger = make_8lab_django_logger1()
