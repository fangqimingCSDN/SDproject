#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : sd_ui.py
@Author  : xiaoming
@Time    : 2023-3-16 18:23
"""
import datetime
import json
import time

import gradio as gr
import os
import pymysql
import uuid
from SDProject.settings import records
import requests
import base64
from PIL import Image
from io import BytesIO
from logger import logger
# ip = records['web_server']
# port = records['web_port']
ip = '127.0.0.1'
port = 8000


def image_to_base64(image: Image.Image,fmt='png') -> str:
    output_buffer = BytesIO()
    image.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return f"data:image/{fmt};base64," + base64_str


def greet(prompt, negative_prompt, image, is_optimize, num_inference_steps, cfg_scale, height, width):
    # pipe = install_v1()
    # ins = install_v1()
    # pipe = ins.pipe
    t0 = time.time()
    logger.info(f"prompt: {prompt}")
    logger.info(f"negative_prompt:{negative_prompt}")
    logger.info(f"image: {image}")
    logger.info(f"is_optimize: {is_optimize}")
    logger.info(f"num_inference_steps:{num_inference_steps}")
    logger.info(f"cfg_scale:{cfg_scale}")
    # logger.info(f"some_pieces  :{some_pieces}")
    logger.info(f"height: {height}")
    logger.info(f"width: {width}")
    # logger.info(f"is_save  :{is_save}")
    if num_inference_steps == 0:
        num_inference_steps = 15
    # if some_pieces == 0:
    #     some_pieces = 1
    # if height == 0:
    #     height = 512 #图片的高度
    # if width == 0:
    #     width = 768 #图片的宽度
    if image:
        images = image_to_base64(image)
        sd_params = {"init_images": [images],"prompt": prompt, "negative_prompt": negative_prompt, "batch_size": 1, "n_iter": 1, "steps": num_inference_steps, "cfg_scale": cfg_scale,"width": width, "height": height}
        service_type = 1
    else:
        sd_params = {"prompt": prompt, "negative_prompt": negative_prompt, "batch_size": 1, "n_iter": 1,
                 "steps": num_inference_steps, "cfg_scale": cfg_scale, "width": width, "height": height}
        service_type = 0
    sd_req_url = f"http://{ip}:{port}/gettask/"
    task_id = str(uuid.uuid1())
    request_params = {
        "task_id": task_id,
        "rqbody": json.dumps(sd_params),
        "service_type": service_type,
        "is_optimize": int(is_optimize)
    }
    step_0 = 0
    try:
        logger.info(f"taskid:{task_id}, 请求的url:{sd_req_url}")
        # logger.info(f"请求参数：{request_params}")
        response = requests.post(url=sd_req_url, json=request_params)
        logger.info('***'*10)
        logger.info(response.text)
        response_info = json.loads(response.text)
    except Exception as e:
        logger.info(f"{task_id}出现错误， 错误原因是：{e}")
        step_0 = 0
    else:
        logger.info(f"taskid：{task_id}成功！")
        step_0 = 1
    if step_0 == 1:
        step_1 = 0
        starttime = datetime.datetime.now()
        endtime = datetime.datetime.now()
        err_index = 0
        images = None
        err_info = None
        while ((starttime - endtime).total_seconds() < 30 * 60):
            time.sleep(5)
            endtime = datetime.datetime.now()
            progress_url = f"http://{ip}:{port}/gettask/?task_id={task_id}"
            try:
                response = requests.get(progress_url, headers={'Content-Type': 'application/json'},
                                        timeout=100)
            except Exception as e:
                logger.info(f"{progress_url},请求失败,报错信息:{e}")
            else:
                logger.info(f"{progress_url},请求成功！")
                result = json.loads(response.text)
                progress = result['progress']
                if progress == -1:
                    err_index += 1
                    logger.info(f"出错，原因是：{result['textinfo']}")
                    err_info = result['textinfo']
                elif progress != 1:
                    logger.info(f"taskid:{task_id}任务完成了{progress}")
                else:
                    step_1 = 1
                    logger.info(f"taskid:{task_id}任务已完成，正在返回图片信息")
                    images = result["current_image"]
                    parameters = result["parameters"]
                    prompt = parameters['prompt']

            finally:
                if step_1 == 1:
                    break
                if err_index >= 3:
                    break
        if step_1 == 1 and err_index < 3:
            imgdata = base64.b64decode(images)
            image = Image.open(BytesIO(imgdata))
        else:
            if err_index >= 3:
                prompt = err_info
            elif step_1 == 0:
                prompt = "任务超时"

    return image, f"查询内容：{prompt}， 耗时：{time.time() - t0}"

iface = gr.Interface(
    fn=greet,
    inputs=[gr.inputs.Textbox(placeholder="描述你想要的图片，中英文均可，强调词科可用括号()，套层数越多强调程度越高，同理减弱词程度使用[]", label="正向提示词"),
            gr.inputs.Textbox(placeholder="描述你不想要的图片，中英文均可，强调词可套用括号()，套层数越多强调程度越高，同理减弱词程度使用[]", label="反向提示词(可选)") ,
            gr.Image(type="pil",shape=(320,320),label="使用图像做提示（可选）"),
            gr.inputs.Checkbox(label="是否对描述的内容进行优化处理(可选)", default=True),
            gr.inputs.Slider(1, 50, default=20, step=1,
            label="生成图片的迭代步数,越高越注重细节， 但是会产生更多的资源消耗"),
    gr.inputs.Slider(3, 16, step=1, default=7, label="参数可变更图像与提示符的一致程度,过高会让图像色彩过于饱和"),
    gr.inputs.Slider(1, 1000, step=1, default=512, label="生成图片高度(像素)"), gr.inputs.Slider(1, 1000, step=1, default=512, label="生成图片宽度(像素)"),],
    outputs=[gr.Image(type="pil",shape=(512,512), label="等待图片返回..."), gr.inputs.Textbox(placeholder="图片返回信息", label="图片返回信息")],
    title="STABLE_DIFFUSIONS 图像生成示例"
)
iface.launch(share=True, inbrowser=True, server_name='0.0.0.0', server_port=7888)
