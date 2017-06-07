# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0004_auto_20160506_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='support_request',
            name='other_app_id',
            field=models.IntegerField(help_text='ID объектов ТО и монтажа', null=True, verbose_name='ID других приложений', blank=True),
        ),
    ]
