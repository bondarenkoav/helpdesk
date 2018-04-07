# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0004_auto_20180119_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opsos_card',
            name='PersonalAccount',
            field=models.CharField(verbose_name='Лицевой счёт', max_length=20),
        ),
    ]
