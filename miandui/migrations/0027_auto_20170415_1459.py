# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-15 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0026_auto_20170415_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='time_login',
            field=models.DateTimeField(default='1970-1-1 00:00:00', verbose_name='\u6700\u540e\u767b\u5f55\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='information',
            name='time_register',
            field=models.DateTimeField(default='1970-1-1 00:00:00', verbose_name='\u6ce8\u518c\u65f6\u95f4'),
        ),
    ]