# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-14 15:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listasprecios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formapago',
            options={'permissions': (('ver_costo_cop', 'Ver Costo Cop'),), 'verbose_name_plural': '1. Formas de Pago'},
        ),
    ]
