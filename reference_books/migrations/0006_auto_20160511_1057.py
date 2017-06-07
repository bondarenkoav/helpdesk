# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reference_books', '0005_auto_20160509_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Send_mail_list',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('GroupName', models.CharField(verbose_name='Наименование группы получателей', max_length=100)),
                ('Subject', models.CharField(verbose_name='Тема письма', max_length=100)),
                ('EmailAddress', models.EmailField(verbose_name='Электронный почтовый адрес', max_length=254)),
                ('Destination', models.ManyToManyField(to=settings.AUTH_USER_MODEL, max_length=2, verbose_name='Получатели ', help_text='Выберите получателей уведомлений')),
                ('ServingCompany', models.ForeignKey(to='reference_books.Company', verbose_name='Сервисная компания')),
            ],
            options={
                'verbose_name': 'Получатель ',
                'verbose_name_plural': 'Список рассылки уведомлений ',
            },
        ),
        migrations.AlterModelOptions(
            name='modeltransmitter',
            options={'verbose_name': 'Модель передатчика', 'verbose_name_plural': 'Список моделей передатчиков '},
        ),
        migrations.AlterModelOptions(
            name='typesecurity',
            options={'verbose_name': 'Тип системы охраны ', 'verbose_name_plural': 'Список системы охраны '},
        ),
        migrations.AlterField(
            model_name='typesecurity',
            name='Decription',
            field=models.CharField(verbose_name='Полное наименование', max_length=100),
        ),
    ]
