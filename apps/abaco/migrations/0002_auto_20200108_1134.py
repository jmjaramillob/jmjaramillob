# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-08 16:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abaco', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regla',
            options={'verbose_name': 'Regla', 'verbose_name_plural': 'Reglas'},
        ),
    ]