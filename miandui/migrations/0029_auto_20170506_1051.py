# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-06 02:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miandui', '0028_auto_20170420_2047'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='information',
            new_name='User',
        ),
    ]
