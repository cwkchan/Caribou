# Generated by Django 2.0.3 on 2018-04-09 18:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubevent',
            name='time',
        ),
        migrations.RemoveField(
            model_name='personalevent',
            name='time',
        ),
        migrations.AddField(
            model_name='clubevent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 9, 14, 16, 3, 823201)),
        ),
        migrations.AddField(
            model_name='clubevent',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 9, 14, 16, 3, 823162)),
        ),
        migrations.AddField(
            model_name='personalevent',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 9, 14, 16, 3, 822183)),
        ),
        migrations.AddField(
            model_name='personalevent',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 9, 14, 16, 3, 822129)),
        ),
        migrations.AlterField(
            model_name='clubevent',
            name='eating_club',
            field=models.CharField(choices=[('NN', 'None'), ('IV', 'The Ivy Club'), ('CT', 'University Cottage Club'), ('TI', 'Tiger Inn'), ('CA', 'Cap and Gown Club'), ('CO', 'Colonial Club'), ('CA', 'Cannon Club'), ('CH', 'Princeton Charter Club'), ('QU', 'Quadrangle Club'), ('TO', ' Princeton Tower Club'), ('TE', 'Terrace Club'), ('CL', 'Cloister Inn')], default='NN', max_length=2),
        ),
        migrations.AlterField(
            model_name='personalevent',
            name='eating_club',
            field=models.CharField(choices=[('NN', 'None'), ('IV', 'The Ivy Club'), ('CT', 'University Cottage Club'), ('TI', 'Tiger Inn'), ('CA', 'Cap and Gown Club'), ('CO', 'Colonial Club'), ('CA', 'Cannon Club'), ('CH', 'Princeton Charter Club'), ('QU', 'Quadrangle Club'), ('TO', ' Princeton Tower Club'), ('TE', 'Terrace Club'), ('CL', 'Cloister Inn')], default='NN', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='clubs_bickering',
            field=models.CharField(choices=[('NN', 'None'), ('IV', 'The Ivy Club'), ('CT', 'University Cottage Club'), ('TI', 'Tiger Inn'), ('CA', 'Cap and Gown Club'), ('CO', 'Colonial Club'), ('CA', 'Cannon Club'), ('CH', 'Princeton Charter Club'), ('QU', 'Quadrangle Club'), ('TO', ' Princeton Tower Club'), ('TE', 'Terrace Club'), ('CL', 'Cloister Inn')], default='NN', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='eating_club',
            field=models.CharField(choices=[('NN', 'None'), ('IV', 'The Ivy Club'), ('CT', 'University Cottage Club'), ('TI', 'Tiger Inn'), ('CA', 'Cap and Gown Club'), ('CO', 'Colonial Club'), ('CA', 'Cannon Club'), ('CH', 'Princeton Charter Club'), ('QU', 'Quadrangle Club'), ('TO', ' Princeton Tower Club'), ('TE', 'Terrace Club'), ('CL', 'Cloister Inn')], default='NN', max_length=2),
        ),
    ]
