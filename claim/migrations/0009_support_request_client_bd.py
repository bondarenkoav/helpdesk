# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0010_merge'),
        ('claim', '0008_auto_20160527_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='support_request',
            name='Client_bd',
            field=models.ForeignKey(verbose_name='Контрагент', blank=True, to='reference_books.Client', help_text='Обязательно для заполнения перед закрытием заявки', null=True),
        ),
    ]
