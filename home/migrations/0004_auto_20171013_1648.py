# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20171013_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='Date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 16, 48, 59, 370160)),
        ),
        migrations.AlterField(
            model_name='attendance_session',
            name='Date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 16, 48, 59, 369247)),
        ),
        migrations.AlterField(
            model_name='logintable',
            name='Start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 16, 48, 59, 371940)),
        ),
    ]
