# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 12:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20171009_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='Date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 9, 12, 19, 15, 467751)),
        ),
        migrations.AlterField(
            model_name='logintable',
            name='Start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 9, 12, 19, 15, 468854)),
        ),
    ]