# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-05 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0016_auto_20170405_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_image',
            field=models.FileField(default=11, upload_to='static/shop', verbose_name='\u5546\u54c1\u56fe\u7247'),
            preserve_default=False,
        ),
    ]
