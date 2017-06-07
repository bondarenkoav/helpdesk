# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objects_to',
            name='TypeSecurity',
            field=models.ManyToManyField(verbose_name='Тип сигнализации', to='reference_books.TypeSecurity'),
        ),
    ]
