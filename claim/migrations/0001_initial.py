# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(verbose_name='Ключ категории')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('mptt_level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='claim.CategoryMenu', null=True, related_name='child', verbose_name='Родитель')),
            ],
            options={
                'verbose_name_plural': 'Дерево меню ',
                'verbose_name': 'Ветка меню ',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Состояние')),
                ('slug', models.SlugField(unique=True, verbose_name='Ключ статуса')),
                ('tr_color', models.CharField(max_length=50, verbose_name='Цвет строки')),
            ],
            options={
                'verbose_name_plural': 'Статусы заявок ',
                'verbose_name': 'Статус заявки ',
            },
        ),
        migrations.CreateModel(
            name='support_request',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.IntegerField(verbose_name='Локальный номер заявки')),
                ('NumObject', models.CharField(max_length=10, verbose_name='№ объекта')),
                ('num_transmitter', models.CharField(blank=True, max_length=15, null=True, verbose_name='Номер передающего устройства')),
                ('AddressObject', models.CharField(max_length=100, verbose_name='Адрес объекта')),
                ('Client', models.CharField(max_length=100, verbose_name='Контрагент')),
                ('Author', models.IntegerField(verbose_name='ID пользователя')),
                ('DateTime_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')),
                ('DateTime_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('FaultAppearance', models.TextField(verbose_name='Вид неисправности')),
                ('DescriptionWorks', models.TextField(blank=True, verbose_name='Что сделали')),
                ('DateTime_schedule', models.DateField(blank=True, null=True, verbose_name='Запланировано на:')),
                ('DateTime_work', models.DateField(blank=True, null=True, verbose_name='Дата и время исполнения')),
                ('Company', models.ForeignKey(to='reference_books.Company', verbose_name='Организация')),
                ('Status', models.ForeignKey(to='claim.Status', default=1, verbose_name='Статус заявки')),
            ],
            options={
                'verbose_name_plural': 'Список заявок ',
                'verbose_name': 'Заявка ',
            },
        ),
        migrations.CreateModel(
            name='TypeRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='Ключ статуса')),
            ],
            options={
                'verbose_name_plural': 'Типы заявок ',
                'verbose_name': 'Тип заявки ',
            },
        ),
        migrations.AddField(
            model_name='support_request',
            name='TypeRequest',
            field=models.ForeignKey(to='claim.TypeRequest', verbose_name='Тип заявки'),
        ),
        migrations.AddField(
            model_name='support_request',
            name='model_transmitter',
            field=models.ForeignKey(blank=True, to='reference_books.ModelTransmitter', null=True, verbose_name='Модель передающего устройства'),
        ),
    ]
