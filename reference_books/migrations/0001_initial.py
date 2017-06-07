# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Город')),
                ('slug', models.SlugField(verbose_name='алиас')),
            ],
            options={
                'verbose_name_plural': 'Список городов ',
                'verbose_name': 'Город ',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, verbose_name='Контрагент')),
            ],
            options={
                'verbose_name_plural': 'Список контрагентов ',
                'verbose_name': 'Контрагент ',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='алиас')),
                ('City', models.ForeignKey(to='reference_books.City', verbose_name='Город')),
            ],
            options={
                'verbose_name_plural': 'Список сервисных компаний ',
                'verbose_name': 'Сервисная компания ',
            },
        ),
        migrations.CreateModel(
            name='CoWorker',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Person_FIO', models.CharField(max_length=100, verbose_name='ФИО сотрудника')),
            ],
            options={
                'verbose_name_plural': 'Список исполнителей ',
                'verbose_name': 'Исполнитель ',
            },
        ),
        migrations.CreateModel(
            name='ExpandedUserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='ФИО пользователя')),
                ('ServingCompany', models.ForeignKey(to='reference_books.Company', verbose_name='Сервисная компания')),
                ('UserName', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя')),
            ],
            options={
                'verbose_name_plural': 'Список профилей пользователей ',
                'verbose_name': 'ДопПрофиль пользователя ',
            },
        ),
        migrations.CreateModel(
            name='ModelTransmitter',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, verbose_name='Модель передатчика')),
            ],
            options={
                'verbose_name_plural': 'Список моделей ПЦН ',
                'verbose_name': 'Модель ',
            },
        ),
        migrations.CreateModel(
            name='Numerate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug_model', models.SlugField(unique=True, verbose_name='Название модели')),
                ('last_num', models.IntegerField(verbose_name='Последний номер')),
                ('ServingCompany', models.ForeignKey(to='reference_books.Company', verbose_name='Сервисная компания')),
            ],
            options={
                'verbose_name_plural': 'Список счетчиков ',
                'verbose_name': 'Счетчик ',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Должность')),
                ('slug', models.SlugField(verbose_name='алиас')),
            ],
            options={
                'verbose_name_plural': 'Список должностей ',
                'verbose_name': 'Должность ',
            },
        ),
        migrations.CreateModel(
            name='SystemPCN',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, verbose_name='Наименование ПЦН')),
            ],
            options={
                'verbose_name_plural': 'Список ПЦН ',
                'verbose_name': 'ПЦН ',
            },
        ),
        migrations.AddField(
            model_name='modeltransmitter',
            name='SystemPCN',
            field=models.ForeignKey(to='reference_books.SystemPCN', verbose_name='Наименование ПЦН'),
        ),
        migrations.AddField(
            model_name='coworker',
            name='Posts',
            field=models.ForeignKey(to='reference_books.Posts', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='coworker',
            name='ServingCompany',
            field=models.ForeignKey(to='reference_books.Company', verbose_name='Сервисная компания'),
        ),
    ]
