# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-13 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('despachos_mercancias', '0008_remove_enviotransportadoratcc_rr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enviotransportadoratcc',
            name='servicio_boom',
        ),
    ]
