# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0012_routesmaintenance'),
        ('maintenance', '0011_auto_20160614_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='trouble_shooting',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('AddressObject', models.CharField(max_length=100, verbose_name='Адрес объекта')),
                ('Client_words', models.CharField(max_length=100, verbose_name='Наименование')),
                ('FaultAppearance', models.TextField(verbose_name='Вид неисправности')),
                ('DescriptionWorks', models.TextField(blank=True, verbose_name='Что сделали')),
                ('DateTime_work', models.DateField(blank=True, verbose_name='Дата и время исполнения', null=True)),
                ('DateTime_add', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')),
                ('DateTime_update', models.DateTimeField(verbose_name='Дата и время обновления', auto_now=True)),
                ('Create_user', models.IntegerField(verbose_name='ID пользователя создавшего заявку')),
                ('Update_user', models.IntegerField(blank=True, verbose_name='ID пользователя закрывшего заявку', null=True)),
                ('Client_bd', models.ForeignKey(blank=True, help_text='Обязательно для заполнения перед закрытием заявки', verbose_name='Контрагент', null=True, to='reference_books.Client')),
                ('CoWorkers', models.ManyToManyField(blank=True, verbose_name='Исполнитель', to='reference_books.CoWorker')),
                ('Company', models.ForeignKey(verbose_name='Организация исполнитель', to='reference_books.Company')),
                ('Status', models.ForeignKey(verbose_name='Статус заявки', default=2, to='reference_books.Status')),
                ('TypeSecurity', models.ManyToManyField(help_text='Выбор нескольких позиций c нажатой кнопкой Ctrl', verbose_name='Тип сигнализации', to='reference_books.TypeSecurity')),
            ],
            options={
                'verbose_name': 'Заявка ',
                'verbose_name_plural': 'Список заявок ',
            },
        ),
        migrations.AddField(
            model_name='objects_to',
            name='Routes',
            field=models.ForeignKey(blank=True, verbose_name='Маршрут', null=True, to='reference_books.RoutesMaintenance'),
        ),
    ]
