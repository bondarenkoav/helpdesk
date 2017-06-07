# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0010_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='coworker',
            name='StatusWorking',
            field=models.BooleanField(help_text='Если сотрудник уволен, снимите галочку', verbose_name='Действующий сотрудник', default=True),
        ),
    ]
