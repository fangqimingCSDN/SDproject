#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : tt1_queue.py
@Author  : xiaoming
@Time    : 2023-5-10 14:24
"""
import threading
from time import time,sleep
from multiprocessing import Queue
maxsize = 10
queue = Queue(maxsize)


class product(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            print("product start...")
            sleep(2)
            print("product done!!!")


class consumer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            print("consumer start...")
            sleep(2)
            print("consumer done!!!")

if __name__ == "__main__":
    threads = []

    t1 = product()
    t2 = consumer()
    threads.append(t1)
    threads.append(t2)
    starttime = time()  #获取执行前的时间
    for t in threads:
        t.setDaemon(True)
        t.start()
    print("done, take time {}".format(time() - starttime))  # 获取执行总的时间
    while True:
        sleep(1)
        print('循环....')

