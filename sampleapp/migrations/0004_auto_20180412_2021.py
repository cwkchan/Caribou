# Generated by Django 2.0.3 on 2018-04-13 00:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0003_auto_20180412_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubevent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 20, 21, 10, 46088)),
        ),
        migrations.AlterField(
            model_name='clubevent',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 20, 21, 10, 46039)),
        ),
        migrations.AlterField(
            model_name='personalevent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 20, 21, 10, 45013)),
        ),
        migrations.AlterField(
            model_name='personalevent',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 20, 21, 10, 44986)),
        ),
    ]
