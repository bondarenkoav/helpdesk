import django_filters

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django_currentuser.db.models import CurrentUserField

from reference_books.models import Client, TypeSecurity, Month_list, ServiceCompanies, CoWorker, ModelTransmitter, \
    Status, TypeRequest, TypeDocument, TypeBuild


class bproposals(models.Model):
    TypeRequest = models.ForeignKey(TypeRequest, models.SET_NULL, verbose_name='Тип заявки',
                                    null=True, blank=True)
    TypeDocument = models.ForeignKey(TypeDocument, models.SET_NULL, verbose_name='Тип документа',
                                     null=True, blank=True)
    TypeBuild = models.ForeignKey(TypeBuild, models.SET_NULL, verbose_name='Тип работ', null=True, blank=True)
    Client_choices = models.ForeignKey(Client, models.SET_NULL, verbose_name='Контрагент', max_length=100, null=True)
    Client_words = models.CharField(max_length=100, blank=True, null=True)
    AddressObject = models.CharField(u'Адрес объекта', max_length=100)
    TypeSecurity = models.ManyToManyField(TypeSecurity, verbose_name='Тип сигнализации',
                                          help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name='Организация', on_delete=models.CASCADE)

    DescriptionWorks = models.TextField(u'Подробное описание', blank=True)
    DateTime_schedule = models.DateField(u'Запланировано на', null=True, blank=True)
    DateTime_work = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    model_transmitter = models.ForeignKey(ModelTransmitter, models.SET_NULL, verbose_name='Модель передатчика',
                                          null=True, blank=True)
    num_transmitter = models.CharField(u'Номер передатчика', max_length=15, null=True, blank=True)
    Status = models.ForeignKey(Status, models.SET_NULL, verbose_name='Статус заявки', default=2, null=True)

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='bp_creator')
    Update_user = CurrentUserField(on_update=True, related_name='bp_modifying')

    def __str__(self):
        return self.AddressObject

    class Meta:
        app_label = 'build'
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок '
        permissions = (
            ('custom_add', u'Добавить заявку'),
            ('custom_view', u'Просмотреть заявку'),
            ('custom_change', u'Изменить заявку'),
            ('change_view_acts', u'Отобразить акты'),
        )


class bproposals_filter(django_filters.FilterSet):
    TypeBuild = django_filters.ModelChoiceFilter(label=u'Тип работ', queryset=TypeBuild.objects.all())
    TypeSecurity = django_filters.ModelChoiceFilter(label=u'Тип системы', queryset=TypeSecurity.objects.all())
    DateTime_schedule = django_filters.DateFilter(label=u'Запланировано', input_formats=('%Y-%m-%d',),
                                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta:
        model = bproposals
        fields = {
            'AddressObject': ['icontains'],
        }


class bacts(models.Model):
    TypeRequest = models.ForeignKey(TypeRequest, models.SET_NULL, verbose_name='Тип заявки', null=True, blank=True)
    TypeDocument = models.ForeignKey(TypeDocument, models.SET_NULL, verbose_name='Тип документа', null=True, blank=True)
    proposal = models.ForeignKey(bproposals, verbose_name='ID заявки на монтаж', on_delete=models.CASCADE)
    Description = models.TextField(u'Подробное описание', null=True, blank=True)
    Day_reporting = models.DateField(u'Отчетный день')
    CoWorkers = models.ManyToManyField(CoWorker, verbose_name='Исполнитель', blank=True)

    DateTime_add = models.DateTimeField(u'Дата создания', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата обновления', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='ba_creator')
    Update_user = CurrentUserField(on_update=True, related_name='ba_modifying')

    class Meta:
        app_label = 'build'
        verbose_name = u'Акт '
        verbose_name_plural = u'Список актов монтажа '
        permissions = (
            ('custom_add_act', u'Добавить акт'),
            ('custom_view_act', u'Просмотреть акт'),
            ('custom_change_act', u'Изменить акт'),
        )
