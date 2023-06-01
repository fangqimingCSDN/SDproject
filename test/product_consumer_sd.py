#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : tt1_queue.py
@Author  : xiaoming
@Time    : 2023-5-10 14:24
"""
import threading
import pymysql
import requests
import json
from time import time,sleep
from multiprocessing import Queue
from SDProject.settings import records
from service_inspection import Inspection
from product_consumer_function import schedule_tag_del
from logger import logger
config={
    "host": records["mysql_host"],
    "port": records["mysql_port"],
    "user": records["mysql_user"],
    "password": records["mysql_password"],
    "database": records['mysql_database'],
    "autocommit": True
}


maxsize = 100



class product(threading.Thread):
    def __init__(self, queue, maxsize):
        super().__init__()
        self.q = queue
        self.maxsize = maxsize
        self.db = pymysql.connect(**config)

    def run(self):
        while True:
            logger.info("product start...")
            # 连接数据库
            self.db.ping(reconnect=True)
            # 使用cursor()方法创建一个游标对象
            self.cursor = self.db.cursor()
            #查询30分钟内的数据（task_id），拉取的最大数据量和队列的最大值相同
            select_sql = f"select t.task_id from sd_task_process t where `status`=0 and TIMESTAMPDIFF(MINUTE, t.create_time, NOW())<=30 ORDER BY t.create_time ASC LIMIT {self.maxsize} ;"
            # logger.info(select_sql)
            self.cursor.execute(select_sql)
            data = self.cursor.fetchall()
            try:
                self.db.commit()
            except Exception as e:
                logger.info(e)
                self.db.rollback()
            logger.info(len([x[0] for x in data]))
            #清空队列
            res = []
            while self.q.qsize() > 0:
                res.append(self.q.get())
            #添加队列数据taskid
            tasklist = [self.q.put(taskid[0]) for taskid in data]
            if self.cursor:
                logger.info('close')
                self.cursor.close()
            self.db.close()
            logger.info(f"product done!!! {len(tasklist)}")
            sleep(2)


class consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.q = queue

    def run(self):
        while True:
            logger.info("consumer start...")
            # 连接数据库
            db = pymysql.connect(**config)
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()

            select_sql = "select ip,port from sd_host where `status`=1;"
            cursor.execute(select_sql)
            data = cursor.fetchall()
            for arg in data:
                ip, port = arg[0], arg[1]
                request_url = f"http://{ip}:{port}/sdapi/v1/progress"
                logger.info(f"查看sd服务主机：{ip}:{port}是否存在空闲任务？")
                logger.info(f"请求的url:{request_url}")
                try:
                    response = requests.get(request_url, headers={'Content-Type': 'application/json'},
                                            timeout=100)
                except Exception as e:
                    logger.info(f"{request_url},请求失败,报错信息:{e}")
                else:
                    result = json.loads(response.text)
                    # logger.info(f"{request_url}, 请求成功， 返回值：{result}")
                    logger.info(f"{request_url}, 请求成功")
                    #data['progress']==0 and data['state']['job_count']==0 为空任务
                    if result['progress'] == 0 and result['state']['job_count']== 0:
                        logger.info(f"sd服务主机：{ip}:{port}存在空闲任务， 开始分配任务")
                        #更新数据库表
                        # if self.q.empty()==True:
                        #     continue
                        taskid = self.q.get()
                        #设置对应taskid记录的ip，host以及更新status为1（准备开始的意思）
                        update_sql = f"update sd_task_process set `ip`='{ip}', `port`='{port}', `status`=1 where task_id='{taskid}';"
                        try:
                            logger.info(update_sql)
                            cursor.execute(update_sql)
                        except pymysql.err.OperationalError as e:
                            logger.info(f"执行{update_sql}数据库连接失败，报错信息：{e},尝试重新连接请求")
                            if cursor:
                                cursor.close()
                            if db:
                                db.close()
                            # 连接数据库
                            db = pymysql.connect(**config)
                            # 使用cursor()方法创建一个游标对象
                            cursor = db.cursor()
                            try:
                                cursor.execute(update_sql)
                            except pymysql.err.OperationalError as e:
                                logger.info(f"执行{update_sql}数据库再次连接失败，报错信息：{e},尝试重新连接请求")
                                if cursor:
                                    cursor.close()
                                if db:
                                    db.close()
                                raise f"数据库连接失败,请检查数据库连接信息,具体{e}"
                        else:
                            logger.info(f"{update_sql}更新成功！")

                        try:
                            db.commit()
                        except Exception as e:
                            db.rollback()
                        logger.info(f"更新数据库中taskid:{taskid}的sd服务信息")

                        #开始执行任务
                        try:
                            select_sql = f"select rqbody,service_type,is_optimize from sd_task_process where `task_id`='{taskid}';"
                            cursor.execute(select_sql)
                            data = cursor.fetchall()
                        except pymysql.err.OperationalError as e:
                            logger.info(f"数据库连接失败，报错信息：{e},尝试重新连接请求")
                            if cursor:
                                cursor.close()
                            if db:
                                db.close()
                            # 连接数据库
                            db = pymysql.connect(**config)
                            # 使用cursor()方法创建一个游标对象
                            cursor = db.cursor()
                            try:
                                select_sql = f"select rqbody,service_type,is_optimize from sd_task_process where `task_id`='{taskid}';"
                                cursor.execute(select_sql)
                                data = cursor.fetchall()
                            except pymysql.err.OperationalError as e:
                                logger.info(f"数据库再次连接失败，报错信息：{e},尝试重新连接请求")
                                if cursor:
                                    cursor.close()
                                if db:
                                    db.close()
                                raise f"数据库连接失败,请检查数据库连接信息,具体{e}"
                        else:
                            logger.info(f"{select_sql}更新成功！")


                        logger.info(f"查询数据库中taskid:{taskid}的rqbody信息")
                        sd_txt2img_req_url = f"http://{ip}:{port}/sdapi/v1/txt2img"
                        sd_img2img_req_url = f"http://{ip}:{port}/sdapi/v1/img2img"
                        request_params = json.loads(data[0][0])
                        service_type = data[0][1]
                        optimize = data[0][2]
                        #############################
                        #处理发生过来的信息， 分词，权重， 翻译
                        if int(optimize) == 1:
                            prompt = ",masterpiece, best quality"
                            no_prompt = ",nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet"
                            request_params['prompt'] = schedule_tag_del(request_params['prompt']) + prompt
                            negative_prompt =  schedule_tag_del(request_params['negative_prompt'])
                            if negative_prompt:
                                negative_prompt = negative_prompt + no_prompt
                            else:
                                negative_prompt = no_prompt[1:]
                            request_params['negative_prompt'] = negative_prompt
                        #############################
                        if service_type == 0:
                            logger.info(f"taskid:{taskid},txt2img开始sd服务请求")
                            t1 = sdRequest(sd_txt2img_req_url, request_params, taskid)
                        else:
                            logger.info(f"taskid:{taskid},img2img开始sd服务请求")
                            t1 = sdRequest(sd_img2img_req_url, request_params, taskid)
                        t1.setDaemon(True)
                        t1.start()


            if cursor:
                cursor.close()
            db.close()
            sleep(2)
            logger.info("consumer done!!!")

class sdRequest(threading.Thread):
    def __init__(self, sd_req_url, request_params, taskid):
        super().__init__()
        self.sd_req_url = sd_req_url
        self.request_params = request_params
        self.request_params_json = json.dumps(request_params,ensure_ascii=False)
        self.task_id = taskid

    def run(self):
        # while True:
        t0 = time()
        logger.info("sdRequest start...")
        # 连接数据库
        db = pymysql.connect(**config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()

        try:
            logger.info(f"taskid:{self.task_id}, 请求的url:{self.sd_req_url}")
            response = requests.post(url=self.sd_req_url, json=self.request_params)
            response_info = json.loads(response.text)
        except Exception as e:
            logger.info(f"{self.task_id}出现错误， 错误原因是：{e}")
            update_sql = f"update sd_task_process set `status`=3 where task_id='{self.task_id}';"
            cursor.execute(update_sql)
            try:
                db.commit()
            except Exception as e:
                db.rollback()
        else:
            logger.info(f"taskid：{self.task_id}成功请求到数据")
            logger.info(f"taskid：{self.task_id}开始更新数据库表")
            # logger.info(response_info)
            images_data = response_info['images'][0]
            update_sql = f"update sd_task_process set `pic_description`='{images_data}', `rqbody`='{self.request_params_json}', `status`=2 where task_id='{self.task_id}';"
            cursor.execute(update_sql)
            try:
                db.commit()
            except Exception as e:
                db.rollback()
            logger.info(f"taskid：{self.task_id}更新成功！")
        finally:
            logger.info(f"taskid:{self.task_id},请求耗时：{time() - t0}")

        if cursor:
            cursor.close()
        db.close()

        logger.info("sdRequest done!!!")



if __name__ == "__main__":
    threads = []
    queue = Queue(maxsize)
    t1 = product(queue, maxsize)
    t2 = consumer(queue)
    t3 = Inspection()
    threads.append((t1, "SD PRODUCT TASK"))
    threads.append((t2, "SD CONSUMER TASK"))
    threads.append((t3, "SD INSPECTION TASK"))
    starttime = time()  #获取执行前的时间
    for t in threads:
        t[0].setDaemon(True)
        t[0].start()
    logger.info("done, take time {}".format(time() - starttime))  # 获取执行总的时间
    while True:
        sleep(10)
        for t in threads:
            label = "死了！"
            if t[0].is_alive():
                label = "活着！"
            logger.info(f"{t[1]}, {label}")  # False. 线程是否存活
        logger.info('循环....')

