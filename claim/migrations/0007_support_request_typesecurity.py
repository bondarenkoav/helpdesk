# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0008_auto_20160516_1550'),
        ('claim', '0006_auto_20160513_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='support_request',
            name='TypeSecurity',
            field=models.ManyToManyField(verbose_name='Тип сигнализации', help_text='Выбор нескольких позиций c нажатой кнопкой Ctrl', to='reference_books.TypeSecurity'),
        ),
    ]
