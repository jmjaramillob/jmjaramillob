# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-09 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrevista', '0013_auto_20200107_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudioentrevista',
            name='codigo',
            field=models.IntegerField(default=2),
        ),
    ]