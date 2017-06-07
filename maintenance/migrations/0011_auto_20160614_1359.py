# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0010_auto_20160609_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance_request',
            name='AddressObject',
        ),
        migrations.RemoveField(
            model_name='maintenance_request',
            name='Client',
        ),
        migrations.RemoveField(
            model_name='maintenance_request',
            name='Company',
        ),
        migrations.RemoveField(
            model_name='maintenance_request',
            name='NumObject',
        ),
        migrations.AlterField(
            model_name='maintenance_request',
            name='Object',
            field=models.ForeignKey(verbose_name='Объект', to='maintenance.objects_to'),
        ),
        migrations.AlterField(
            model_name='maintenance_request',
            name='TypeSecurity',
            field=models.CharField(blank=True, verbose_name='Объём работ', null=True, max_length=100),
        ),
    ]
