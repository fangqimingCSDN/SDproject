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
# 写一个快速排序算法
def quick_sort(lists, left, right):
	# 快速排序
	if left >= right:
		return lists
	key = lists[left]
	low = left
	high = right
	while left < right:
		while left < right and lists[right] >= key:
			right -= 1
		lists[left] = lists[right]
		while left < right and lists[left] <= key:
			left += 1
		lists[right] = lists[left]
	lists[right] = key
	quick_sort(lists, low, left - 1)
	quick_sort(lists, left + 1, high)
	return lists


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