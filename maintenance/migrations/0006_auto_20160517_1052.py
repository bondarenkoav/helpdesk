# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0005_objects_to_date_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objects_to',
            name='Month_schedule',
            field=models.ManyToManyField(help_text='Выбор нескольких позиций c нажатой кнопкой Ctrl', null=True, verbose_name='Месяцы обслуживания', blank=True, to='reference_books.Month_list'),
        ),
        migrations.AlterField(
            model_name='objects_to',
            name='TypeSecurity',
            field=models.ManyToManyField(help_text='Выбор нескольких позиций c нажатой кнопкой Ctrl', to='reference_books.TypeSecurity', verbose_name='Тип сигнализации'),
        ),
    ]
