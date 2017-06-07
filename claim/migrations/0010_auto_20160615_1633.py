# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0009_support_request_client_bd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support_request',
            name='Client',
            field=models.CharField(verbose_name='Наименование', max_length=100),
        ),
    ]
