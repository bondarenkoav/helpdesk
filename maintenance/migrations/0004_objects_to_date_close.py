# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0003_remove_objects_to_year_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='objects_to',
            name='Date_close',
            field=models.DateField(null=True, verbose_name='Дата окончания обслуживания', help_text='Указываем последний день обслуживания', blank=True),
        ),
    ]
