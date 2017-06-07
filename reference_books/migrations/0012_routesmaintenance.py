# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0011_coworker_statusworking'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutesMaintenance',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('Number', models.SmallIntegerField(verbose_name='Номер маршрута')),
                ('Descript', models.TextField(help_text='Введите последовательно населённые пункты данного маршрута', verbose_name='Описание маршрута')),
            ],
            options={
                'verbose_name': 'Маршрут ',
                'verbose_name_plural': 'Список маршрутов ТО ',
            },
        ),
    ]
