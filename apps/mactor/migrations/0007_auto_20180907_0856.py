# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-07 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0006_estudiomactor_diasfinalizacioninforme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estudiomactor',
            old_name='diasFinalizacionInforme',
            new_name='dias_finalizacion_informe',
        ),
    ]
