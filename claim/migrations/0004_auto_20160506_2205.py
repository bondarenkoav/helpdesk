# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0003_auto_20160505_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support_request',
            name='model_transmitter',
            field=models.ForeignKey(null=True, verbose_name='Модель передатчика', to='reference_books.ModelTransmitter', blank=True),
        ),
        migrations.AlterField(
            model_name='support_request',
            name='num_transmitter',
            field=models.CharField(null=True, verbose_name='Номер передатчика', max_length=15, blank=True),
        ),
    ]
