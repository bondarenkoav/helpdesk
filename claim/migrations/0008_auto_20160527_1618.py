# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0007_support_request_typesecurity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='support_request',
            name='TypeRequest',
        ),
        migrations.RemoveField(
            model_name='support_request',
            name='custom_id',
        ),
        migrations.RemoveField(
            model_name='support_request',
            name='other_app_id',
        ),
        migrations.AlterField(
            model_name='support_request',
            name='Status',
            field=models.ForeignKey(default=2, to='reference_books.Status', verbose_name='Статус заявки'),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
