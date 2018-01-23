# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reference_books', '0015_event_opsos_name_opsos_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='logging',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('application', models.SlugField(verbose_name='Приложение', max_length=30)),
                ('old_value', models.CharField(verbose_name='Старое значение', max_length=100, null=True, blank=True)),
                ('add_date', models.DateTimeField(verbose_name='Дата и время записи', auto_now_add=True)),
                ('event_code', models.ForeignKey(to='reference_books.Event', verbose_name='Событие')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Событие ',
                'verbose_name_plural': 'Журнал событий ',
            },
        ),
    ]
