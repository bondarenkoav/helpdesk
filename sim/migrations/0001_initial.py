# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference_books', '0015_event_opsos_name_opsos_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpSoS_card',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('Number_SIM', models.IntegerField(verbose_name='Номер сим-карты')),
                ('ICC_SIM', models.CharField(verbose_name='Ид.код сим-карты', max_length=20)),
                ('Contract', models.CharField(verbose_name='Договор', max_length=100)),
                ('Contract_date', models.DateField(verbose_name='Дата')),
                ('PersonalAccount', models.IntegerField(verbose_name='Лицевой счёт')),
                ('Use_numberobject', models.CharField(verbose_name='Номер объекта', max_length=30, blank=True)),
                ('Use_addressobject', models.CharField(verbose_name='Адрес объекта', max_length=300, blank=True)),
                ('Use_user', models.CharField(verbose_name='Фамилия Имя Отчество', max_length=100, blank=True)),
                ('Notation', models.TextField(verbose_name='Примечание', null=True, blank=True)),
                ('Status', models.BooleanField(verbose_name='SIM-карта активна', default=True)),
                ('DateTime_add', models.DateTimeField(verbose_name='Дата и время добавления', auto_now_add=True)),
                ('DateTime_update', models.DateTimeField(verbose_name='Дата и время обновления', auto_now=True)),
                ('Create_user', models.IntegerField(verbose_name='ID пользователя создавшего запись')),
                ('Update_user', models.IntegerField(verbose_name='ID пользователя изменившего запись', null=True, blank=True)),
                ('OpSoSRate', models.ForeignKey(to='reference_books.OpSoS_rate', max_length=100, verbose_name='Тариф')),
                ('Owner', models.ForeignKey(to='reference_books.Company', verbose_name='Контрагент оператора')),
            ],
            options={
                'verbose_name': 'СИМ-карта ',
                'verbose_name_plural': 'Список сим-карт ',
            },
        ),
        migrations.CreateModel(
            name='UseTypeSIM',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('Name', models.CharField(verbose_name='Название', max_length=100)),
                ('slug', models.SlugField(verbose_name='алиас')),
            ],
            options={
                'verbose_name': 'Тип ',
                'verbose_name_plural': 'Типы применения SIM-карт ',
            },
        ),
        migrations.AddField(
            model_name='opsos_card',
            name='Use_type',
            field=models.ForeignKey(to='sim.UseTypeSIM', verbose_name='Тип применения'),
        ),
    ]
