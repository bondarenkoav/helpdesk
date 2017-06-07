# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0012_routesmaintenance'),
        ('maintenance', '0012_auto_20160920_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='trouble_shooting',
            name='Routes',
            field=models.ForeignKey(blank=True, null=True, verbose_name='Маршрут', to='reference_books.RoutesMaintenance'),
        ),
    ]
