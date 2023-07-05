#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : tt.py
@Author  : xiaoming
@Time    : 2023-5-10 8:16
"""

import pymysql
import requests
import json
from time import time,sleep
from multiprocessing import Queue
from SDProject.settings import records
config={
    "host": records["mysql_host"],
    "port": records["mysql_port"],
    "user": records["mysql_user"],
    "password": records["mysql_password"],
    "database": records['mysql_database']
}
# 写一个验证身份证号码，手机号码，邮箱的正则表达式
import re
def check_fun(password):
	iphone_re = re.compile(r'^1[3-9]\d{9}$')
	idcard_re = re.compile(r'^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1-2]\d|3[01])\d{3}[\dxX]$')
	email_re = re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
	if iphone_re.match(password):
		print("手机号码")
	elif idcard_re.match(password):
		print("身份证号码")
	elif email_re.match(password):
		print("邮箱")
	else:
		print("输入有误")

# 写一个冒泡排序算法
def bubble_sort(lists):
	# 冒泡排序
	count = len(lists)
	for i in range(0, count):
		for j in range(i + 1, count):
			if lists[i] > lists[j]:
				lists[i], lists[j] = lists[j], lists[i]
	return lists

# Write a singleton pattern independently
class Singleton(object):
	__instance = None
	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = object.__new__(cls, *args, **kwargs)
		return cls.__instance

# 写一个装饰器，限制函数被调用的频率
def limit_fun(fun):
	def inner(*args,**kwargs):
		print("装饰器开始")
		fun(*args,**kwargs)
		print("装饰器结束")
	return inner

@limit_fun
def test_fun():
	print("函数开始")
	sleep(2)
	print("函数结束")

# 写一个函数，接收一个参数，返回参数的类型
def type_fun(param):
	return type(param)




if __name__ == '__main__':
	# 连接数据库
	db = pymysql.connect(**config)
	# 使用cursor()方法创建一个游标对象
	cursor = db.cursor()
	#查询30分钟内的数据（task_id），拉取的最大数据量和队列的最大值相同
	# select_sql = f"select t.task_id from sd_task_process t where `status`=0 and TIMESTAMPDIFF(MINUTE, t.create_time, NOW())>0 and TIMESTAMPDIFF(MINUTE, t.create_time, NOW())<=30 ORDER BY t.create_time ASC LIMIT 100 ;"
	select_sql = f"select rqbody,service_type from sd_task_process where `task_id`='21199';"
	cursor.execute(select_sql)
	data = cursor.fetchall()
	print(data)
	print(data[0][0])
	print(data[0][1]==0)
	# # print([x[0] for x in data])
	# select_sql = f"select rqbody from sd_task_process where `task_id`={21203};"
	# cursor.execute(select_sql)
	# data = cursor.fetchall()
	# print(type(data[0][0]))
	# print(json.loads(data[0][0]))
	# import time
	# print("20230515140323")
	# timestamp = time.time()
	# timestruct = time.localtime(timestamp)
	# ct = time.strftime('%Y%m%d%H%M%S', timestruct)
	# print(ct)
	a = {
		"skipped": False,
		"interrupted": False,
		"job": "",
		"job_count": 1,
		"job_timestamp": 1
	}
	b = {"fang": "fangqiming"}
	a.update(b)
	print(a)