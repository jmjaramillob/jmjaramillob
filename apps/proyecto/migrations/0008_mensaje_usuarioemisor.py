# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-25 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0007_auto_20200123_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='usuarioEmisor',
            field=models.TextField(blank=True, null=True),
        ),
    ]
