# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0006_auto_20160511_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='send_mail_list',
            name='Message',
            field=models.TextField(help_text='В тексте письма обязательно должен находится тег %object%', default='', verbose_name='Текст письма'),
            preserve_default=False,
        ),
    ]
