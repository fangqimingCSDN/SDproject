# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2023-05-09 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sd_interface', '0002_auto_20230509_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='sd_task_process',
            name='rqbody',
            field=models.TextField(blank=True, null=True, verbose_name='请求体'),
        ),
    ]
