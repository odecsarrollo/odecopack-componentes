# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VtigerAccount',
            fields=[
                ('accountid', models.IntegerField(primary_key=True, serialize=False)),
                ('account_no', models.CharField(max_length=100)),
                ('accountname', models.CharField(max_length=100)),
                ('parentid', models.IntegerField(blank=True, null=True)),
                ('account_type', models.CharField(blank=True, max_length=200, null=True)),
                ('industry', models.CharField(blank=True, max_length=200, null=True)),
                ('annualrevenue', models.DecimalField(blank=True, decimal_places=8, max_digits=25, null=True)),
                ('rating', models.CharField(blank=True, max_length=200, null=True)),
                ('ownership', models.CharField(blank=True, max_length=50, null=True)),
                ('siccode', models.CharField(blank=True, max_length=50, null=True)),
                ('tickersymbol', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('otherphone', models.CharField(blank=True, max_length=30, null=True)),
                ('email1', models.CharField(blank=True, max_length=100, null=True)),
                ('email2', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('fax', models.CharField(blank=True, max_length=30, null=True)),
                ('employees', models.IntegerField(blank=True, null=True)),
                ('emailoptout', models.CharField(blank=True, max_length=3, null=True)),
                ('notify_owner', models.CharField(blank=True, max_length=3, null=True)),
                ('isconvertedfromlead', models.CharField(blank=True, max_length=3, null=True)),
            ],
            options={
                'db_table': 'vtiger_account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VtigerAccountscf',
            fields=[
                ('accountid', models.IntegerField(primary_key=True, serialize=False)),
                ('cf_751', models.CharField(blank=True, max_length=10, null=True)),
                ('cf_753', models.CharField(blank=True, max_length=10, null=True)),
                ('cf_787', models.TextField(blank=True, null=True)),
                ('cf_789', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'vtiger_accountscf',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VtigerCrmentity',
            fields=[
                ('crmid', models.IntegerField(primary_key=True, serialize=False)),
                ('smcreatorid', models.IntegerField()),
                ('modifiedby', models.IntegerField()),
                ('setype', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('createdtime', models.DateTimeField()),
                ('modifiedtime', models.DateTimeField()),
                ('viewedtime', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('version', models.IntegerField()),
                ('presence', models.IntegerField(blank=True, null=True)),
                ('deleted', models.IntegerField()),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'vtiger_crmentity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VtigerUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_password', models.CharField(blank=True, max_length=200, null=True)),
                ('user_hash', models.CharField(blank=True, max_length=32, null=True)),
                ('cal_color', models.CharField(blank=True, max_length=25, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('reports_to_id', models.CharField(blank=True, max_length=36, null=True)),
                ('is_admin', models.CharField(blank=True, max_length=3, null=True)),
                ('currency_id', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('date_entered', models.DateTimeField()),
                ('date_modified', models.DateTimeField(blank=True, null=True)),
                ('modified_user_id', models.CharField(blank=True, max_length=36, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_home', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_work', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_other', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_fax', models.CharField(blank=True, max_length=50, null=True)),
                ('email1', models.CharField(blank=True, max_length=100, null=True)),
                ('email2', models.CharField(blank=True, max_length=100, null=True)),
                ('secondaryemail', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=25, null=True)),
                ('signature', models.TextField(blank=True, null=True)),
                ('address_street', models.CharField(blank=True, max_length=150, null=True)),
                ('address_city', models.CharField(blank=True, max_length=100, null=True)),
                ('address_state', models.CharField(blank=True, max_length=100, null=True)),
                ('address_country', models.CharField(blank=True, max_length=25, null=True)),
                ('address_postalcode', models.CharField(blank=True, max_length=9, null=True)),
                ('user_preferences', models.TextField(blank=True, null=True)),
                ('tz', models.CharField(blank=True, max_length=30, null=True)),
                ('holidays', models.CharField(blank=True, max_length=60, null=True)),
                ('namedays', models.CharField(blank=True, max_length=60, null=True)),
                ('workdays', models.CharField(blank=True, max_length=30, null=True)),
                ('weekstart', models.IntegerField(blank=True, null=True)),
                ('date_format', models.CharField(blank=True, max_length=200, null=True)),
                ('hour_format', models.CharField(blank=True, max_length=30, null=True)),
                ('start_hour', models.CharField(blank=True, max_length=30, null=True)),
                ('end_hour', models.CharField(blank=True, max_length=30, null=True)),
                ('activity_view', models.CharField(blank=True, max_length=200, null=True)),
                ('lead_view', models.CharField(blank=True, max_length=200, null=True)),
                ('imagename', models.CharField(blank=True, max_length=250, null=True)),
                ('deleted', models.IntegerField()),
                ('confirm_password', models.CharField(blank=True, max_length=300, null=True)),
                ('internal_mailer', models.CharField(max_length=3)),
                ('reminder_interval', models.CharField(blank=True, max_length=100, null=True)),
                ('reminder_next_time', models.CharField(blank=True, max_length=100, null=True)),
                ('crypt_type', models.CharField(max_length=20)),
                ('accesskey', models.CharField(blank=True, max_length=36, null=True)),
                ('theme', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.CharField(blank=True, max_length=36, null=True)),
                ('time_zone', models.CharField(blank=True, max_length=200, null=True)),
                ('currency_grouping_pattern', models.CharField(blank=True, max_length=100, null=True)),
                ('currency_decimal_separator', models.CharField(blank=True, max_length=2, null=True)),
                ('currency_grouping_separator', models.CharField(blank=True, max_length=2, null=True)),
                ('currency_symbol_placement', models.CharField(blank=True, max_length=20, null=True)),
                ('phone_crm_extension', models.CharField(blank=True, max_length=100, null=True)),
                ('no_of_currency_decimals', models.CharField(blank=True, max_length=2, null=True)),
                ('truncate_trailing_zeros', models.CharField(blank=True, max_length=3, null=True)),
                ('dayoftheweek', models.CharField(blank=True, max_length=100, null=True)),
                ('callduration', models.CharField(blank=True, max_length=100, null=True)),
                ('othereventduration', models.CharField(blank=True, max_length=100, null=True)),
                ('calendarsharedtype', models.CharField(blank=True, max_length=100, null=True)),
                ('default_record_view', models.CharField(blank=True, max_length=10, null=True)),
                ('leftpanelhide', models.CharField(blank=True, max_length=3, null=True)),
                ('rowheight', models.CharField(blank=True, max_length=10, null=True)),
                ('defaulteventstatus', models.CharField(blank=True, max_length=50, null=True)),
                ('defaultactivitytype', models.CharField(blank=True, max_length=50, null=True)),
                ('hidecompletedevents', models.IntegerField(blank=True, null=True)),
                ('is_owner', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'vtiger_users',
                'managed': False,
            },
        ),
    ]
