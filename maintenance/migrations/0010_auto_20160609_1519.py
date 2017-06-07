# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0009_maintenance_request_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance_request',
            name='Object',
            field=models.IntegerField(verbose_name='Объект'),
        ),
    ]
