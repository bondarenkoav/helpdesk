# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0010_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='acts_build',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=10, default='Акт')),
                ('Description', models.TextField(blank=True, null=True, verbose_name='Подробное описание')),
                ('Day_reporting', models.DateField(verbose_name='Отчетный день')),
                ('DateTime_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('DateTime_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('Create_user', models.IntegerField(verbose_name='ID пользователя создавшего заявку')),
                ('Update_user', models.IntegerField(blank=True, null=True, verbose_name='ID пользователя закрывшего заявку')),
                ('CoWorkers', models.ManyToManyField(to='reference_books.CoWorker', blank=True, verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name_plural': 'Список актов монтажа ',
                'verbose_name': 'Акт ',
            },
        ),
        migrations.CreateModel(
            name='build_request',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('AddressObject', models.CharField(max_length=100, verbose_name='Адрес объекта')),
                ('Create_user', models.IntegerField(verbose_name='ID пользователя создавшего заявку')),
                ('Update_user', models.IntegerField(blank=True, null=True, verbose_name='ID пользователя закрывшего заявку')),
                ('DateTime_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')),
                ('DateTime_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')),
                ('DescriptionWorks', models.TextField(blank=True, verbose_name='Подробное описание')),
                ('DateTime_schedule', models.DateField(blank=True, null=True, verbose_name='Запланировано на')),
                ('DateTime_work', models.DateField(blank=True, null=True, verbose_name='Дата и время исполнения')),
                ('num_transmitter', models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер передатчика')),
                ('Client', models.ForeignKey(max_length=100, to='reference_books.Client', verbose_name='Контрагент')),
                ('Company', models.ForeignKey(to='reference_books.Company', verbose_name='Организация')),
                ('Status', models.ForeignKey(to='reference_books.Status', default=2, verbose_name='Статус заявки')),
            ],
            options={
                'verbose_name_plural': 'Список заявок ',
                'verbose_name': 'Заявка ',
            },
        ),
        migrations.CreateModel(
            name='TypeRequest_build',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='Ключ статуса')),
            ],
            options={
                'verbose_name_plural': 'Типы заявок ',
                'verbose_name': 'Тип заявки ',
            },
        ),
        migrations.AddField(
            model_name='build_request',
            name='TypeRequest',
            field=models.ForeignKey(to='build.TypeRequest_build', verbose_name='Тип монтажа'),
        ),
        migrations.AddField(
            model_name='build_request',
            name='TypeSecurity',
            field=models.ManyToManyField(help_text='Выбор нескольких позиций c нажатой кнопкой Ctrl', to='reference_books.TypeSecurity', verbose_name='Тип сигнализации'),
        ),
        migrations.AddField(
            model_name='build_request',
            name='model_transmitter',
            field=models.ForeignKey(to='reference_books.ModelTransmitter', verbose_name='Модель передатчика', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='acts_build',
            name='build_request',
            field=models.ForeignKey(to='build.build_request', verbose_name='ID заявки на монтаж'),
        ),
    ]
