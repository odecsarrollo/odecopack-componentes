# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-02 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biable', '0043_auto_20170202_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='CiudadBiable',
            fields=[
                ('ciudad_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='DepartamentoBiable',
            fields=[
                ('departamento_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PaisBiable',
            fields=[
                ('pais_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='departamentobiable',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biable.PaisBiable'),
        ),
        migrations.AddField(
            model_name='ciudadbiable',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biable.DepartamentoBiable'),
        ),
    ]
