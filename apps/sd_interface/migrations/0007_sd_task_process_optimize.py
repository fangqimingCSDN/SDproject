# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2023-05-24 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sd_interface', '0006_sd_task_process_service_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sd_task_process',
            name='optimize',
            field=models.IntegerField(default=0, verbose_name='0：不优化权重参数，1: 优化权重参数'),
        ),
    ]