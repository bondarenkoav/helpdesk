# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0007_auto_20160527_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance_request',
            name='TypeSecurity',
        ),
        migrations.AddField(
            model_name='maintenance_request',
            name='TypeSecurity',
            field=models.CharField(default='', verbose_name='Объём работ', max_length=100),
            preserve_default=False,
        ),
    ]
