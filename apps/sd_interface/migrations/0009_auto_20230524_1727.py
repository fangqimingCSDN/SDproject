# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2023-05-24 17:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sd_interface', '0008_auto_20230524_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sd_task_process',
            old_name='is_ptimize',
            new_name='is_optimize',
        ),
    ]