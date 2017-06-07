# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0002_support_request_coworkers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='support_request',
            name='Author',
        ),
        migrations.AddField(
            model_name='support_request',
            name='Create_user',
            field=models.IntegerField(default=1, verbose_name='ID пользователя создавшего заявку'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='support_request',
            name='Update_user',
            field=models.IntegerField(null=True, verbose_name='ID пользователя закрывшего заявку', blank=True),
        ),
    ]
