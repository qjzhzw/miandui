# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-14 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0021_auto_20170407_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='date_sign_in',
            field=models.DateField(null=True, verbose_name='\u6700\u8fd1\u7b7e\u5230\u65e5\u671f'),
        ),
    ]
