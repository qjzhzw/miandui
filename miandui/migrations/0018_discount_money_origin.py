# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-05 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0017_shop_shop_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='money_origin',
            field=models.DecimalField(decimal_places=2, default=12, max_digits=5, verbose_name='\u539f\u4ef7'),
            preserve_default=False,
        ),
    ]
