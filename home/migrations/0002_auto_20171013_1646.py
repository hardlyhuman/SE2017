# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissions',
            name='Sub_Status',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='Date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 16, 46, 46, 65988)),
        ),
        migrations.AlterField(
            model_name='attendance_session',
            name='Date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 16, 46, 46, 65057)),
        ),
        migrations.AlterField(
            model_name='logintable',
            name='Start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 16, 46, 46, 67779)),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='End_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Start_time',
            field=models.TimeField(),
        ),
    ]
