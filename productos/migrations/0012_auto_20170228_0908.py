# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 14:08
from __future__ import unicode_literals

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0011_remove_articulocatalogo_id_cguno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
