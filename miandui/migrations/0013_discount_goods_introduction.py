# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-28 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0012_auto_20170328_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='goods_introduction',
            field=models.CharField(default=11, max_length=100, verbose_name='\u5546\u54c1\u4ecb\u7ecd'),
            preserve_default=False,
        ),
    ]
