# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0009_status'),
        ('maintenance', '0006_auto_20160517_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='maintenance_request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('NumObject', models.CharField(verbose_name='№ объекта', max_length=10)),
                ('AddressObject', models.CharField(verbose_name='Адрес объекта', max_length=100)),
                ('Client', models.CharField(verbose_name='Контрагент', max_length=100)),
                ('Create_user', models.IntegerField(verbose_name='ID пользователя создавшего заявку')),
                ('Update_user', models.IntegerField(null=True, verbose_name='ID пользователя закрывшего заявку', blank=True)),
                ('DateTime_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')),
                ('DateTime_update', models.DateTimeField(verbose_name='Дата и время обновления', auto_now=True)),
                ('DescriptionWorks', models.TextField(verbose_name='Что сделали', blank=True)),
                ('DateTime_schedule', models.DateField(null=True, verbose_name='Запланировано на:', blank=True)),
                ('DateTime_work', models.DateField(null=True, verbose_name='Дата и время исполнения', blank=True)),
                ('CoWorkers', models.ManyToManyField(to='reference_books.CoWorker', verbose_name='Исполнитель', blank=True)),
                ('Company', models.ForeignKey(to='reference_books.Company', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Заявка ',
                'verbose_name_plural': 'Список заявок ',
            },
        ),
        migrations.RenameModel(
            old_name='Status',
            new_name='Status_object',
        ),
        migrations.AddField(
            model_name='maintenance_request',
            name='Status',
            field=models.ForeignKey(default=2, to='reference_books.Status', verbose_name='Статус заявки'),
        ),
        migrations.AddField(
            model_name='maintenance_request',
            name='TypeSecurity',
            field=models.ManyToManyField(help_text='Выбор нескольких позиций c нажатой кнопкой Ctrl', to='reference_books.TypeSecurity', verbose_name='Тип сигнализации'),
        ),
    ]
