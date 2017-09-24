# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='Password',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='End_Time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 23, 19, 20, 54, 520408)),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='Start_Time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 22, 19, 20, 54, 520371)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='Date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 22, 19, 20, 54, 517920)),
        ),
        migrations.AlterField(
            model_name='logintable',
            name='Start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 22, 19, 20, 54, 519535)),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='Sub_Time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 22, 19, 20, 54, 521286)),
        ),
    ]
