# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-09 01:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abaco', '0002_auto_20200108_1134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idea',
            old_name='idProponente',
            new_name='idCreador',
        ),
        migrations.AddField(
            model_name='idea',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
    ]