# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0014_auto_20170117_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='en_edicion',
            field=models.BooleanField(default=False),
        ),
    ]
