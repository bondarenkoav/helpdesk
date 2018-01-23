# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0014_transmitter_serial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('Name', models.CharField(verbose_name='Наименование события', max_length=200, unique=True)),
                ('slug', models.SlugField(verbose_name='Алиас', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Событие ',
                'verbose_name_plural': 'События ',
            },
        ),
        migrations.CreateModel(
            name='OpSoS_name',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('Name', models.CharField(verbose_name='Наименование', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Сотовый оператор',
                'verbose_name_plural': 'Список сотовых операторов ',
            },
        ),
        migrations.CreateModel(
            name='OpSoS_rate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('Rate', models.CharField(verbose_name='Наименование', max_length=100, unique=True)),
                ('Descript', models.TextField(verbose_name='Описание тарифа')),
                ('OpSoSName', models.ForeignKey(to='reference_books.OpSoS_name', verbose_name='Сотовый оператор')),
            ],
            options={
                'verbose_name': 'Тариф ',
            },
        ),
    ]
