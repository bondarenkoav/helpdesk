# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0014_auto_20180125_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='support_request',
            name='Date_act',
            field=models.DateField(verbose_name='Дата предоставления акта', default='2018-01-01', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='support_request',
            name='Required_act',
            field=models.BooleanField(verbose_name='Требуется акт выполненных работ', default=False),
        ),
    ]
