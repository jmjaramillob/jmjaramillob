# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 03:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mactor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='descripcion',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ficha',
            name='estrategia',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='objetivo',
            name='descripcion',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='actor',
            unique_together=set([('nombreCorto', 'idEstudio'), ('nombreLargo', 'idEstudio'), ('nombreLargo', 'nombreCorto', 'idEstudio')]),
        ),
        migrations.AlterUniqueTogether(
            name='objetivo',
            unique_together=set([('nombreCorto', 'idEstudio'), ('nombreLargo', 'idEstudio'), ('nombreLargo', 'nombreCorto', 'idEstudio')]),
        ),
    ]