#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : tt1.py
@Author  : xiaoming
@Time    : 2023-5-25 11:21
"""
import threading
from time import sleep


def demo_func_one():
    sleep(1)
    print("demo one")


def demo_func_two():
    while True:
        for i in range(5):
            sleep(1)
            print("demo two")
            print("当前线程： ", threading.current_thread())  # <Thread(Thread-2, started 11952)>


def demo_func_three():
    while True:
        sleep(1)
        print("demo three")
        print("当前活动线程", threading.active_count())  # 4, 三个子线程 一个主线程

# 添加守护线程
def demo_func_four():
    while True:
        sleep(1)
        print("demo four")
        print("当前活动线程", threading.active_count())  # 4, 三个子线程 一个主线程




if __name__ == '__main__':
    func_list = [demo_func_one, demo_func_two, demo_func_three]
    thread_list = []
    print("主线程", threading.main_thread())  # <_MainThread(MainThread, started 3948)>
    for func in func_list:
        t = threading.Thread(target=func)
        thread_list.append(t)
        t.setDaemon(True)  # 设置线程为守护线程
        t.start()  # 开始线程
        print("线程是否存活：", t.is_alive())  # True，线程是否存活

    # for t in thread_list:
    #     t.join()  # 等待，直到线程终结。这会阻塞调用这个方法的线程，直到被调用 join() 的线程终结 -

    for t in thread_list:
        print(t.is_alive())  # False. 线程是否存活

    while True:
        sleep(2)
        print("循环...")
        for t in thread_list:
            print(t.is_alive())  # False. 线程是否存活

# 主线程默认不是守护线程，主线程创建的子线程默认也不是守护线程