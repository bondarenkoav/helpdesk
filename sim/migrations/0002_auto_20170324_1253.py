# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-24 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsos_card',
            name='Number_SIM',
            field=models.BigIntegerField(verbose_name='Номер сим-карты'),
        ),
    ]
