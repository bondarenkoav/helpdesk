# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0005_support_request_other_app_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support_request',
            name='Status',
            field=models.ForeignKey(to='claim.Status', verbose_name='Статус заявки', default=2),
        ),
    ]
