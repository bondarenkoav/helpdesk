# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0004_objects_to_date_close'),
    ]

    operations = [
        migrations.AddField(
            model_name='objects_to',
            name='Date_open',
            field=models.DateField(default='2016-01-01', verbose_name='Дата начала обслуживания'),
            preserve_default=False,
        ),
    ]
