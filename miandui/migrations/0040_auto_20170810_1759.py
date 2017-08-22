# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0039_order_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordergoods',
            name='order',
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='identification',
            field=models.IntegerField(default=1, verbose_name='\u8d26\u53f7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='phone',
            field=models.IntegerField(default=1, verbose_name='\u624b\u673a\u53f7'),
            preserve_default=False,
        ),
    ]
