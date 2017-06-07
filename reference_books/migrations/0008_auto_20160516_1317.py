# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0007_send_mail_list_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='Name',
            field=models.CharField(max_length=100, verbose_name='Контрагент'),
        ),
    ]
