# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0004_month_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='objects_to',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('NumObject', models.CharField(max_length=10, verbose_name='№ объекта')),
                ('AddressObject', models.CharField(max_length=100, verbose_name='Адрес объекта')),
                ('Year_schedule', models.IntegerField(verbose_name='Год обслуживания')),
                ('DateTime_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания плана')),
                ('DateTime_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления плана')),
                ('Create_user', models.IntegerField(verbose_name='ID пользователя создавшего заявку')),
                ('Update_user', models.IntegerField(verbose_name='ID пользователя закрывшего заявку', blank=True, null=True)),
                ('Client', models.ForeignKey(to='reference_books.Client', max_length=100, verbose_name='Контрагент')),
                ('Month_schedule', models.ManyToManyField(verbose_name='Месяцы обслуживания', blank=True, to='reference_books.Month_list', null=True)),
                ('ServingCompany', models.ForeignKey(to='reference_books.Company', verbose_name='Организация')),
            ],
            options={
                'verbose_name_plural': 'Список объектов ТО ',
                'verbose_name': 'Объект ',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Состояние')),
                ('slug', models.SlugField(unique=True, verbose_name='Ключ статуса')),
            ],
            options={
                'verbose_name_plural': 'Статусы объетов ТО ',
                'verbose_name': 'Статус объекта ',
            },
        ),
        migrations.AddField(
            model_name='objects_to',
            name='Status',
            field=models.ForeignKey(to='maintenance.Status', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='objects_to',
            name='TypeSecurity',
            field=models.ManyToManyField(to='reference_books.TypeSecurity', verbose_name='Организация'),
        ),
    ]
