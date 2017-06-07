# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0008_auto_20160516_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('Name', models.CharField(verbose_name='Состояние', max_length=100)),
                ('slug', models.SlugField(verbose_name='Ключ статуса', unique=True)),
                ('tr_color', models.CharField(verbose_name='Цвет строки', max_length=50)),
            ],
            options={
                'verbose_name': 'Статус заявки ',
                'verbose_name_plural': 'Статусы заявок ',
            },
        ),
    ]
