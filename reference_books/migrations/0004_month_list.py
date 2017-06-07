# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0003_typesecurity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month_list',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('Month_num', models.CharField(max_length=2, verbose_name='Номер месяца')),
                ('Month_name', models.CharField(max_length=50, verbose_name='Название месяца')),
            ],
            options={
                'verbose_name_plural': 'Список месяцев ',
                'verbose_name': 'Месяц ',
            },
        ),
    ]
