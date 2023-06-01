#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : forms.py
@Author  : xiaoming
@Time    : 2023-5-9 16:47
"""

from apps.sd_interface.models import SD_Host, SD_Task_Process
from django import forms



class SD_Task_ProcessForm(forms.ModelForm):
    ip = forms.CharField(required=False)
    port = forms.CharField(required=False)
    status = forms.IntegerField(required=False)
    pic_description = forms.Textarea()
    create_time = forms.DateTimeField(required=False)
    service_type = forms.IntegerField(required=False)
    is_optimize = forms.IntegerField(required=False)



    def clean_port(self):
        port = self.data.get("port")
        if not port:
            pass
        return port

    def clean_ip(self):
        ip = self.data.get("ip")
        if not ip:
            pass
        return ip

    def clean_status(self):
        status = self.data.get("status")
        if not status:
            pass
        return status

    def clean_pic_description(self):
        pic_description = self.data.get("pic_description")
        if not pic_description:
            pass
        return pic_description

    def clean_create_time(self):
        create_time = self.data.get("create_time")
        if not create_time:
            pass
        return create_time


    def clean_task_id(self):
        task_id = self.data.get("task_id")
        if not task_id:
            raise forms.ValidationError("task_id不能为空！")
        return task_id

    def clean_rqbody(self):
        rqbody = self.data.get("rqbody")
        if not rqbody:
            raise forms.ValidationError("rqbody不能为空！")
        return rqbody

    def clean_service_type(self):
        service_type = self.data.get("service_type")
        if not service_type:
            pass
        return service_type

    def clean_is_optimize(self):
        is_optimize = self.data.get("is_optimize")
        if not is_optimize:
            pass
        return is_optimize


    class Meta:
        model = SD_Task_Process
        fields = '__all__'