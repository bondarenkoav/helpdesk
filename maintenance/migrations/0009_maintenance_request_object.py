# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0008_auto_20160606_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance_request',
            name='Object',
            field=models.ForeignKey(default=1, to='maintenance.objects_to', verbose_name='Объект', max_length=10),
            preserve_default=False,
        ),
    ]
