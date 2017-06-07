# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numerate',
            name='slug_model',
            field=models.SlugField(verbose_name='Название модели'),
        ),
    ]
