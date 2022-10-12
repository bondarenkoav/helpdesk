import django_filters

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
# from django_currentuser.middleware import get_current_authenticated_user

from reference_books.models import Client, TypeSecurity, Month_list, ServiceCompanies, CoWorker, Status, \
    RoutesMaintenance, TypeRequest, TypeDocument


class mobjects(models.Model):
    TypeRequest = models.ForeignKey(TypeRequest, models.SET_NULL, verbose_name=u'Тип заявки', null=True, blank=True)
    TypeDocument = models.ForeignKey(TypeDocument, models.SET_NULL, verbose_name=u'Тип документа', null=True, blank=True)
    NumObject = models.CharField(u'№ объекта', max_length=10)
    AddressObject = models.CharField(u'Адрес объекта', max_length=300)
    Client_choices = models.ForeignKey(Client, models.SET_NULL, verbose_name=u'Контрагент', max_length=100, null=True)
    Client_words = models.CharField(max_length=100, blank=True, null=True)
    Routes = models.ForeignKey(RoutesMaintenance, models.SET_NULL, verbose_name=u'Маршрут', null=True, blank=True)
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name=u'Организация', on_delete=models.CASCADE)
    TypeSecurity = models.ManyToManyField(TypeSecurity, verbose_name=u'Тип сигнализации',
                                          help_text=u'Выбор нескольких позиций c нажатой кнопкой Ctrl')
    Month_schedule = models.ManyToManyField(Month_list, verbose_name=u'Месяцы обслуживания',
                                            help_text=u'Выбор нескольких позиций c нажатой кнопкой Ctrl', blank=True)
    Date_open = models.DateField(u'Дата начала обслуживания')
    Date_end = models.DateField(u'Дата окончания обслуживания', help_text=u'Указываем последний день обслуживания',
                                null=True, blank=True)
    Status_object = models.BooleanField(u'Обслуживается', default=False)

    DateTime_add = models.DateTimeField(u'Дата создания плана', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата обновления плана', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='mo_creator')
    Update_user = CurrentUserField(on_update=True, related_name='mo_modifying')

    def __str__(self):
        return self.NumObject

    class Meta:
        app_label = 'maintenance'
        verbose_name = u'Объект '
        verbose_name_plural = u'Список объектов ТО '
        permissions = (
            ('custom_add_object', u'Добавить объект'),
            ('custom_view_object', u'Просмотреть объект'),
            ('custom_change_object', u'Изменить объект'),
        )


class mobjects_filter(django_filters.FilterSet):
    AddressObject = django_filters.CharFilter(label=u'Адрес объекта', widget=forms.TextInput())
    Routes = django_filters.ModelChoiceFilter(label=u'Маршрут', queryset=RoutesMaintenance.objects.all())
    Month_schedule = django_filters.ModelChoiceFilter(label=u'Месяц', queryset=Month_list.objects.all())
    TypeSecurity = django_filters.ModelMultipleChoiceFilter(queryset=TypeSecurity.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = mobjects
        fields = ['NumObject', 'AddressObject', 'Routes', 'Status_object', 'Month_schedule', 'TypeSecurity']


class mproposals(models.Model):
    TypeRequest = models.ForeignKey(TypeRequest, models.SET_NULL,
                                    verbose_name=u'Тип заявки', null=True, blank=True)
    TypeDocument = models.ForeignKey(TypeDocument, models.SET_NULL,
                                     verbose_name=u'Тип документа', null=True, blank=True)
    Object = models.ForeignKey(mobjects, verbose_name=u'Объект', on_delete=models.CASCADE)
    DescriptionWorks = models.TextField(u'Что сделали', blank=True)
    DateTime_schedule = models.DateField(u'Запланировано на:', null=True, blank=True)
    DateTime_work = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    CoWorkers = models.ManyToManyField(CoWorker, verbose_name=u'Исполнитель', blank=True)
    Status = models.ForeignKey(Status, models.SET_NULL, null=True, verbose_name=u'Статус заявки', default=2)

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='mp_creator')
    Update_user = CurrentUserField(on_update=True, related_name='mp_modifying')

    def __str__(self):
        return self.Object.AddressObject

    class Meta:
        app_label = 'maintenance'
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок ТО'
        permissions = (
            ('custom_add', u'Добавить заявку ТО'),
            ('custom_view', u'Просмотреть заявку ТО'),
            ('custom_change', u'Изменить заявку ТО'),
        )


class mproposals_filter(django_filters.FilterSet):
    class Meta:
        model = mproposals
        fields = []


class mtroubles(models.Model):
    TypeRequest = models.ForeignKey(TypeRequest, models.SET_NULL, verbose_name=u'Тип заявки',
                                    null=True, blank=True)
    TypeDocument = models.ForeignKey(TypeDocument, models.SET_NULL, verbose_name=u'Тип документа',
                                     null=True, blank=True)
    AddressObject = models.CharField(u'Адрес объекта', max_length=100)
    TypeSecurity = models.ManyToManyField(TypeSecurity, verbose_name=u'Тип сигнализации',
                                          help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")
    Client_choices = models.ForeignKey(Client, models.SET_NULL, verbose_name=u'Контрагент',
                                       help_text="Обязательно для заполнения перед закрытием заявки",
                                       null=True, blank=True)
    Client_words = models.CharField(u'Наименование', max_length=100, null=True, blank=True)
    Routes = models.ForeignKey(RoutesMaintenance, models.SET_NULL, verbose_name=u'Маршрут', null=True, blank=True)
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name=u'Организация исполнитель',
                                       on_delete=models.CASCADE)
    FaultAppearance = models.TextField(u'Вид неисправности')
    DescriptionWorks = models.TextField(u'Что сделали', blank=True)
    DateTime_work = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    CoWorkers = models.ManyToManyField(CoWorker, verbose_name=u'Исполнитель', blank=True)
    Status = models.ForeignKey(Status, models.SET_NULL, null=True, verbose_name=u'Статус заявки', default=2)

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='mt_creator')
    Update_user = CurrentUserField(on_update=True, related_name='mt_modifying')

    def __str__(self):
        return self.AddressObject

    class Meta:
        app_label = 'maintenance'
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок на устранение неисправностей '
        permissions = (
            ('custom_add_trouble', u'Добавить заявку на устранение'),
            ('custom_view_trouble', u'Просмотреть заявку на устранение'),
            ('custom_change_trouble', u'Изменить заявку на устранение'),
        )


class mtroubles_filter(django_filters.FilterSet):
    Routes = django_filters.ModelChoiceFilter(queryset=RoutesMaintenance.objects.all(), label=u'Маршрут')
    Status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label=u'Статус заявки')

    class Meta:
        model = mtroubles
        fields = ['AddressObject', 'Routes', 'Status']


class count_completeproposals_per_month(models.Model):
    dmonth = models.CharField(max_length=100)
    dyear = models.CharField(max_length=100)

    class Meta:
        managed = False
