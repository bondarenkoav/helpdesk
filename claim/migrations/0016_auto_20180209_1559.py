# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0015_auto_20180209_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support_request',
            name='Date_act',
            field=models.DateField(blank=True, null=True, verbose_name='Дата предоставления акта'),
        ),
    ]
