# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0004_month_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='typesecurity',
            name='Decription',
            field=models.CharField(default='', verbose_name='Аббревиатура', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='typesecurity',
            name='Name',
            field=models.CharField(verbose_name='Аббревиатура', max_length=10),
        ),
    ]
