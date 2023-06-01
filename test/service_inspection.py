#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : service_inspection.py
@Author  : xiaoming
@Time    : 2023-5-12 10:33
"""
import threading
import requests
import json
from time import sleep, time
import pymysql
from SDProject.settings import records
from logger import logger
config={
    "host": records["mysql_host"],
    "port": records["mysql_port"],
    "user": records["mysql_user"],
    "password": records["mysql_password"],
    "database": records['mysql_database']
}



class Inspection(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            logger.info("Inspection start...")
            ###循环检查主机状态， 是否激活服务
            # 连接数据库
            db = pymysql.connect(**config)
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()

            select_sql = "select * from sd_host"
            cursor.execute(select_sql)
            data = cursor.fetchall()
            #[('101.42.242.227', '7860', 0), ('192.168.1.192', '7860', 0)]
            for arg in data:
                status = 0
                ip = arg[0]
                port = arg[1]
                request_url = f"http://{ip}:{port}/sdapi/v1/progress"
                logger.info(request_url)
                try:
                    response = requests.get(request_url, headers={'Content-Type': 'application/json'},
                                            timeout=100)
                except Exception as e:
                    logger.info(f"{request_url},请求失败,报错信息:{e}")
                    status = 0
                else:
                    if response.status_code==200:
                        result = json.loads(response.text)
                        progress = -1
                        if type(result) == dict:
                            progress = result.get("progress", -1)
                        logger.info(f"{request_url}, 请求成功， 返回值：{progress}")
                        status = 1
                    else:
                        logger.info(f"{request_url}, 请求失败， 返回值：{response.status_code}")
                        status = 0
                finally:
                    update_sql = f"update sd_host set `status`={status} where ip='{ip}';"
                    cursor.execute(update_sql)
                    try:
                        db.commit()
                    except Exception as e:
                        db.rollback()


            if cursor:
                cursor.close()
            db.close()
            sleep(10)
            logger.info("Inspection done!!!")


if __name__ == "__main__":
    threads = []

    t1 = Inspection()
    threads.append(t1)
    starttime = time()  #获取执行前的时间
    for t in threads:
        t.setDaemon(True)
        t.start()
    logger.info("done, take time {}".format(time() - starttime))  # 获取执行总的时间
    while True:
        sleep(20)
        logger.info('循环....')


