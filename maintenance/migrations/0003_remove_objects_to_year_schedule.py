# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0002_auto_20160509_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objects_to',
            name='Year_schedule',
        ),
    ]
