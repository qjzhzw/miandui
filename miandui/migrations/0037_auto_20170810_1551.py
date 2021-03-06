# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0036_order_goodss'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=20, verbose_name='\u5546\u54c1\u540d\u79f0')),
                ('money_need', models.CharField(max_length=10, verbose_name='\u6240\u9700\u91d1\u94b1')),
                ('goods_number', models.IntegerField(default=999, null=True, verbose_name='\u5546\u54c1\u6570\u91cf')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u5546\u54c1\u4fe1\u606f',
                'verbose_name_plural': '\u8ba2\u5355\u5546\u54c1\u4fe1\u606f',
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='goodss',
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_goods', to='miandui.Order'),
        ),
    ]
