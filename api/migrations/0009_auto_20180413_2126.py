# Generated by Django 2.0.3 on 2018-04-14 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180413_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubevent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 13, 21, 26, 51, 628599)),
        ),
        migrations.AlterField(
            model_name='clubevent',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 13, 21, 26, 51, 628599)),
        ),
        migrations.AlterField(
            model_name='personalevent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 13, 21, 26, 51, 627748)),
        ),
        migrations.AlterField(
            model_name='personalevent',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 13, 21, 26, 51, 627748)),
        ),
    ]
