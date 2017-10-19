# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-05 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.IntegerField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'rooms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ss234024',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('time', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ss234024',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tt234024',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('time', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '弹幕统计',
                'verbose_name_plural': '弹幕统计',
                'db_table': 'tt234024',
                'managed': False,
            },
        ),
    ]