# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-10 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abaco', '0005_auto_20200110_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
