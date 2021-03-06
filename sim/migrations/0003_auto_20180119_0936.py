# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-01-19 04:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0015_event_opsos_name_opsos_rate'),
        ('sim', '0002_auto_20170324_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='opsos_card',
            name='SystemPCN',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reference_books.SystemPCN', verbose_name='ПЦН'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opsos_card',
            name='Use_nameobject',
            field=models.CharField(blank=True, max_length=300, verbose_name='Наименование объекта'),
        ),
    ]
