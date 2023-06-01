#!/bin/bash


nohup python3 -u manage.py runserver 0.0.0.0:8888 > web.log 2>&1  &
nohup python3 -u  product_consumer_sd.py > product_consumer.log 2>&1 &
nohup python3 -u sd_ui.py > sdui.log 2>&1 &
nohup python3 -u gradio_monitor.py  >monitor.log 2>&1 &