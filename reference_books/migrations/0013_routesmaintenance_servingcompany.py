# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0012_routesmaintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='routesmaintenance',
            name='ServingCompany',
            field=models.ForeignKey(to='reference_books.Company', verbose_name='Сервисная компания', default=1),
            preserve_default=False,
        ),
    ]
