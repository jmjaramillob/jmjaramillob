# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-01-12 22:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abaco', '0020_opcionescala_codigocolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escala',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='opcionescala',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]