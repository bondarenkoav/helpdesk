# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0001_initial'),
        ('claim', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='support_request',
            name='CoWorkers',
            field=models.ManyToManyField(to='reference_books.CoWorker', blank=True, verbose_name='Исполнитель'),
        ),
    ]
