# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-12 21:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abaco', '0018_auto_20200112_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='escala',
            old_name='titulo',
            new_name='nombre',
        ),
    ]
