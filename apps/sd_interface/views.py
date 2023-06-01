import json

import requests
import time
from django.shortcuts import render

# Create your views here.
# from django.views.generic.base import View
# from rest_framework import generics
from rest_framework.response import Response
from apps.sd_interface.models import SD_Task_Process
from apps.sd_interface.forms import SD_Task_ProcessForm
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
# from apps.view_utils.logger import logger
import logging
# 实例化logging对象,并以当前文件的名字作为logger实例的名字
logger = logging.getLogger(__name__)
# 生成一个名字叫做 loggers.apps 的日志实例
logger_c = logging.getLogger('loggers.apps')
# #获取task_id并记录在表sd_task_process中
# from SDProject.settings import queue, maxsize


class GetTaskid_intodb(APIView):
    """ 获取task_id并记录在表sd_task_process中 """

    def get(self,  request, *args, **kwargs):
        """巡检，查看进度使用接口"""
        timestamp = time.time()
        timestruct = time.localtime(timestamp)
        ct = time.strftime('%Y%m%d%H%M%S', timestruct)
        t0 = time.time()
        logger.info(f"GetTaskid_intodb GET start...")
        task_id = request.GET['task_id']
        task_obj = SD_Task_Process.objects.filter(task_id=task_id).order_by('-create_time').first()
        if not task_obj:
            reponse_info = {
                "progress": -1,
                "eta_relative": time.time() - t0,
                "state": {
                    "skipped": None,
                    "interrupted": None,
                    "job": "",
                    "job_count": 0,
                    "job_timestamp": f"{ct}",
                    "job_no": 1,
                    "sampling_step": 0,
                    "sampling_steps": 20
                },
                "parameters": None,
                "current_image": None,
                "textinfo": "无此任务taskid"
            }

            return Response(reponse_info)
        elif task_obj.status == 0: #任务未开始介入到任务
            logger.info(f"GetTaskid_intodb GET  inspect status {task_obj.status} completed, time: {time.time() - t0}")
            reponse_info = {
                "progress": 0,
                "eta_relative": time.time() - t0,
                "state": {
                    "skipped": None,
                    "interrupted": None,
                    "job": "",
                    "job_count": 0,
                    "job_timestamp": f"{ct}",
                    "job_no": 1,
                    "sampling_step": 0,
                    "sampling_steps": 20
                },
                "parameters": json.loads(task_obj.rqbody),
                "current_image": None,
                "textinfo": "Waiting..."
            }
            return Response(reponse_info)
        elif task_obj.status == 1:  #任务正在开始执行
            request_url = f"http://{task_obj.ip}:{task_obj.port}/sdapi/v1/progress"
            try:
                response = requests.get(request_url, headers={'Content-Type': 'application/json'},
                                        timeout=30)
            except Exception as e:
                logger.error(e)
                # logger.info('false')
                reponse_info = {
                    "progress": -1,
                    "eta_relative": time.time() - t0,
                    "state": {
                        "skipped": None,
                        "interrupted": None,
                        "job": "",
                        "job_count": 0,
                        "job_timestamp": f"{ct}",
                        "job_no": 1,
                        "sampling_step": 0,
                        "sampling_steps": 20
                    },
                    "parameters": json.loads(task_obj.rqbody),
                    "current_image": None,
                    "textinfo": f"任务执行失败， 失败原因：{e}"
                }
                return Response(reponse_info)
            else:
                result = json.loads(response.text)
                logger.info(f"GetTaskid_intodb GET  inspect status {task_obj.status} completed, time: {time.time() - t0}")
                return Response(result)
        elif task_obj.status == 2:  #任务成功执行完成
            #查询数据库并返回image数据，最后设置status标识为
            reponse_info = {
                "progress": 1,
                "eta_relative": time.time() - t0,
                "state": {
                    "skipped": None,
                    "interrupted": None,
                    "job": "",
                    "job_count": 0,
                    "job_timestamp": f"{ct}",
                    "job_no": 1,
                    "sampling_step": 0,
                    "sampling_steps": 20
                },
                "parameters": json.loads(task_obj.rqbody),
                "current_image": f'{task_obj.pic_description}',
                "textinfo": "成功返回"
            }
            # task_obj.delete()
            # logger.info(f"{task_obj.task_id},记录删除成功！")
            logger.info(f"GetTaskid_intodb GET  inspect status {task_obj.status} completed, time: {time.time() - t0}")
            return Response(reponse_info)
        elif task_obj.status == 3: #操作失败任务
            logger.info(f"GetTaskid_intodb GET  inspect status {task_obj.status} completed, time: {time.time() - t0}")
            reponse_info = {
                "progress": -1,
                "eta_relative": time.time() - t0,
                "state": {
                    "skipped": None,
                    "interrupted": None,
                    "job": "",
                    "job_count": 0,
                    "job_timestamp": f"{ct}",
                    "job_no": 1,
                    "sampling_step": 0,
                    "sampling_steps": 20
                },
                "parameters": json.loads(task_obj.rqbody),
                "current_image": None,
                "textinfo": "操作失败任务"
            }
            # task_obj.delete()
            # logger.info(f"{task_obj.task_id},记录删除成功！")
            return Response(reponse_info)
        else: #其他情况， 如status == 4 已完成任务--未使用标签
            logger.info(f"GetTaskid_intodb GET  inspect status {task_obj.status} completed, time: {time.time() - t0}")
            reponse_info = {
                "progress": -1,
                "eta_relative": time.time() - t0,
                "state": {
                    "skipped": None,
                    "interrupted": None,
                    "job": "",
                    "job_count": 0,
                    "job_timestamp": f"{ct}",
                    "job_no": 1,
                    "sampling_step": 0,
                    "sampling_steps": 20
                },
                "parameters": json.loads(task_obj.rqbody),
                "current_image": None,
                "textinfo": "非法状态标记"
            }
            return Response(reponse_info)


    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        """添加服务请求任务， 记录到队列中"""
        sd_form = SD_Task_ProcessForm(request.data)
        request_taskid = request.data.get("task_id")
        task_id = SD_Task_Process.objects.filter(task_id=request.data.get("task_id")).first()
        if not task_id:
            logger.info(f'task_id:{request_taskid}进入！')
            if sd_form.is_valid():
                sd_form.save()
                logger.info(f'task_id:{request_taskid}已保存！')
            else:
                logger.info(sd_form.is_valid())
                logger.info(sd_form.errors)
        else:
            logger.info(f'task_id:{task_id.task_id}, 已存在！！')
            if sd_form.is_valid():
                sd_form.save()
                logger.info(f'task_id:{task_id.task_id}, 已替换！！')
            else:
                logger.info(sd_form.is_valid())
                logger.info(sd_form.errors)
                return Response({"code": 500, "message": str(sd_form.errors)})

        return Response({"code":200, "message": 'finish'})