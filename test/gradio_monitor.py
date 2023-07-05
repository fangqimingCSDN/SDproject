#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : gradio_monitor.py
@Author  : xiaoming
@Time    : 2023-5-10 14:47
"""
import gradio as gr
# from django.db import connection
from SDProject.settings import records
import pymysql
from logger import logger

config={
    "host": records["mysql_host"],
    "port": records["mysql_port"],
    "user": records["mysql_user"],
    "password": records["mysql_password"],
    "database": records['mysql_database']
}


def calculator(sdHost, sdPort, operation):
    logger.info(f"sdHost:{sdHost}, sdPort:{sdPort}, operation:{operation}")
    if operation == "query_table":
        # 连接数据库
        db = pymysql.connect(**config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        data = []
        select_sql = "select * from sd_host"
        try:
            cursor.execute(select_sql)
            data = cursor.fetchall()
        except pymysql.err.OperationalError as e:
            logger.info(f"查询数据库失败， select_sql：{select_sql} 失败原因：{e}")
            if cursor:
                cursor.close()
            if db:
                db.close()
            # 连接数据库
            db = pymysql.connect(**config)
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()
            select_sql = "select * from sd_host"
            try:
                cursor.execute(select_sql)
                data = cursor.fetchall()
            except pymysql.err.OperationalError as e:
                logger.info(f"查询数据库失败， select_sql：{select_sql} 失败原因：{e}")
                if cursor:
                    cursor.close()
                if db:
                    db.close()
                raise f"查询数据库失败， select_sql：{select_sql} 失败原因：{e}"
        else:
            logger.info(f"{select_sql}查询成功！")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
        return [x for x in data]
    elif operation == "add_host":

        # 连接数据库
        db = pymysql.connect(**config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        # insert_sql = f"insert into sd_host (ip, port, status) values ('{sdHost}','{sdPort}', 0)"
        # cursor.execute(insert_sql)
        # try:
        #     db.commit()
        # except Exception as e:
        #     db.rollback()
        # finally:
        #     if cursor:
        #         cursor.close()
        #     db.close()

        insert_sql = f"insert into sd_host (ip, port, status) values ('{sdHost}','{sdPort}', 0)"
        try:
            cursor.execute(insert_sql)
            db.commit()
        except pymysql.err.OperationalError as e:
            logger.info(f"操作数据库失败， insert_sql：{insert_sql} 失败原因：{e}， 开始回滚重试")
            db.rollback()
            # raise f"查询数据库失败， select_sql：{select_sql} 失败原因：{e}"
            if cursor:
                cursor.close()
            if db:
                db.close()
            # 连接数据库
            db = pymysql.connect(**config)
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()
            insert_sql = f"insert into sd_host (ip, port, status) values ('{sdHost}','{sdPort}', 0)"
            try:
                cursor.execute(insert_sql)
                db.commit()
            except pymysql.err.OperationalError as e:
                logger.info(f"操作数据库失败， insert_sql：{insert_sql} 失败原因：{e}， 开始回滚! 抛出异常")
                db.rollback()
                if cursor:
                    cursor.close()
                if db:
                    db.close()
                raise f"查询数据库失败， insert_sql：{select_sql} 失败原因：{e}"
        except Exception as e:
            logger.info(f"操作数据库失败， insert_sql：{insert_sql} 失败原因：{e}， 开始回滚! 抛出异常")
            db.rollback()
            if cursor:
                cursor.close()
            if db:
                db.close()
            raise f"查询数据库失败， insert_sql：{insert_sql} 失败原因：{e}"
        else:
            logger.info(f"{insert_sql}操作成功！")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
        return calculator(sdHost, sdPort, 'query_table')
    elif operation == "remove_host":
        # 连接数据库
        db = pymysql.connect(**config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        remove_sql = f"delete from sd_host where ip='{sdHost}'"
        cursor.execute(remove_sql)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            if cursor:
                cursor.close()
            db.close()

        remove_sql = f"delete from sd_host where ip='{sdHost}'"
        try:
            cursor.execute(remove_sql)
            db.commit()
        except pymysql.err.OperationalError as e:
            logger.info(f"操作数据库失败， remove_sql：{remove_sql} 失败原因：{e}， 开始回滚重试")
            db.rollback()
            # raise f"查询数据库失败， select_sql：{select_sql} 失败原因：{e}"
            if cursor:
                cursor.close()
            if db:
                db.close()
            # 连接数据库
            db = pymysql.connect(**config)
            # 使用cursor()方法创建一个游标对象
            cursor = db.cursor()
            remove_sql = f"delete from sd_host where ip='{sdHost}'"
            try:
                cursor.execute(remove_sql)
                db.commit()
            except pymysql.err.OperationalError as e:
                logger.info(f"操作数据库失败， remove_sql：{remove_sql} 失败原因：{e}， 开始回滚! 抛出异常")
                db.rollback()
                if cursor:
                    cursor.close()
                if db:
                    db.close()
                raise f"查询数据库失败， remove_sql：{remove_sql} 失败原因：{e}"
        except Exception as e:
            logger.info(f"操作数据库失败， remove_sql：{remove_sql} 失败原因：{e}， 开始回滚! 抛出异常")
            db.rollback()
            if cursor:
                cursor.close()
            if db:
                db.close()
            raise f"查询数据库失败， remove_sql：{remove_sql} 失败原因：{e}"
        else:
            logger.info(f"{remove_sql}操作成功！")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
        return calculator(sdHost, sdPort, 'query_table')



iface = gr.Interface(
    fn=calculator,
    inputs=['text', 'text', gr.inputs.Radio(["query_table", "add_host", "remove_host"])],
    live=False,#如果任何输入改变，接口是否应该自动重新运行。
    # 设置输出
    outputs="text",
    # 设置输入参数示例
    examples=[
        ['192.168.1.191', "7860"],
        ['101.42.242.227', "7860"],
    ],
    # 设置网页标题
    title="监控主机状态",
    # 左上角的描述文字
    description="1. 添加监控的主机，2. 查询主机的状态信息 ",
    # 左下角的文字
    article = "Check out the examples"
)

# iface.launch(share=True, inbrowser=True, server_name='0.0.0.0', server_port=7666)
iface.launch(share=True)