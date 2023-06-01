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

config={
    "host": records["mysql_host"],
    "port": records["mysql_port"],
    "user": records["mysql_user"],
    "password": records["mysql_password"],
    "database": records['mysql_database']
}


def calculator(sdHost, sdPort, operation):
    if operation == "query_table":
        # 连接数据库
        db = pymysql.connect(**config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()

        select_sql = "select * from sd_host"
        cursor.execute(select_sql)
        data = cursor.fetchall()
        if cursor:
            cursor.close()
        db.close()
        return [x for x in data]
    elif operation == "add_host":
        # 连接数据库
        db = pymysql.connect(**config)
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        insert_sql = f"insert into sd_host (ip, port, status) values ('{sdHost}','{sdPort}', 0)"
        cursor.execute(insert_sql)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            if cursor:
                cursor.close()
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