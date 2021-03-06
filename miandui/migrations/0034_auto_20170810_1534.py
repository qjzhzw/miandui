# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0033_auto_20170517_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.IntegerField(verbose_name='\u8d26\u53f7')),
                ('time_arrive', models.DateTimeField(null=True, verbose_name='\uff08\u9884\u8ba1\uff09\u5230\u8fbe\u65f6\u95f4')),
                ('money_discount', models.CharField(max_length=10, verbose_name='\u5546\u5bb6\u6d3b\u52a8\u4f18\u60e0')),
                ('money_service', models.CharField(max_length=10, verbose_name='\u5e73\u53f0\u670d\u52a1\u8d39')),
                ('status', models.IntegerField(default=1, verbose_name='\u72b6\u6001')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u4fe1\u606f',
                'verbose_name_plural': '\u8ba2\u5355\u4fe1\u606f',
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='identification',
            field=models.IntegerField(default=1, verbose_name='\u8d26\u53f7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='password',
            field=models.CharField(default=1, max_length=20, verbose_name='\u5bc6\u7801'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goods',
            name='goods_number',
            field=models.IntegerField(default=999, null=True, verbose_name='\u5546\u54c1\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='order',
            name='goodss',
            field=models.ManyToManyField(to='miandui.Goods'),
        ),
    ]
