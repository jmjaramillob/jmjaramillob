# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-12 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0003_auto_20180714_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='nombreLargo',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='objetivo',
            name='nombreLargo',
            field=models.CharField(max_length=150),
        ),
    ]
