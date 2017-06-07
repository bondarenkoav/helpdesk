# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-03 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0013_routesmaintenance_servingcompany'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transmitter_serial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=50, verbose_name='Модель устройства')),
                ('Transmitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reference_books.ModelTransmitter', verbose_name='Номер серийный устройства')),
            ],
            options={
                'verbose_name_plural': 'Список серйиных номеров устройств ',
                'verbose_name': 'Серийный номер',
            },
        ),
    ]
