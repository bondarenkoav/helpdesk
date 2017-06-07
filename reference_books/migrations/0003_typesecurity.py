# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0002_auto_20160503_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeSecurity',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, verbose_name='')),
                ('slug', models.SlugField(unique=True, verbose_name='Алиас')),
            ],
            options={
                'verbose_name_plural': 'Список ПЦН ',
                'verbose_name': 'ПЦН ',
            },
        ),
    ]
