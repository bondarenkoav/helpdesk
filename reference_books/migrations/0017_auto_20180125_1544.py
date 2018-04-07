# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0016_opsos_rate_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsos_rate',
            name='price',
            field=models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Абонентская плата', default=0),
        ),
    ]
