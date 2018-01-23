# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsos_card',
            name='Number_SIM',
            field=models.BigIntegerField(verbose_name='Номер сим-карты'),
        ),
    ]
