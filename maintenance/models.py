from django.db import models
from reference_books.models import Client, TypeSecurity, Month_list, Company, CoWorker, Status, RoutesMaintenance


class Status_object(models.Model):
    Name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Статус объекта '
        verbose_name_plural = u'Статусы объетов ТО '

class objects_to(models.Model):
    NumObject           = models.CharField(u'№ объекта',max_length=10)
    Date_open           = models.DateField(u'Дата начала обслуживания')
    AddressObject       = models.CharField(u'Адрес объекта', max_length=100)
    Client              = models.ForeignKey(Client,verbose_name='Контрагент', max_length=100)
    Routes              = models.ForeignKey(RoutesMaintenance,verbose_name='Маршрут',null=True,blank=True)
    ServingCompany      = models.ForeignKey(Company, verbose_name='Организация')
    TypeSecurity        = models.ManyToManyField(TypeSecurity, verbose_name='Тип сигнализации', help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")
    Month_schedule      = models.ManyToManyField(Month_list, verbose_name='Месяцы обслуживания', help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl", null=True, blank=True)
    Date_close          = models.DateField(u'Дата окончания обслуживания', help_text='Указываем последний день обслуживания', null=True, blank=True)
    Status              = models.ForeignKey(Status_object, verbose_name='Статус')
    DateTime_add        = models.DateTimeField(u'Дата создания плана', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата обновления плана', auto_now=True)
    Create_user         = models.IntegerField(u'ID пользователя создавшего заявку')
    Update_user         = models.IntegerField(u'ID пользователя закрывшего заявку', null=True, blank=True)
    def __str__(self):  return self.NumObject
    class Meta:
        verbose_name = u'Объект '
        verbose_name_plural = u'Список объектов ТО '

class maintenance_request(models.Model):
    Object              = models.ForeignKey(objects_to,verbose_name='Объект')
    TypeSecurity        = models.CharField(u'Объём работ', null=True, blank=True, max_length=300)
    Create_user         = models.IntegerField(u'ID пользователя создавшего заявку')
    Update_user         = models.IntegerField(u'ID пользователя закрывшего заявку', null=True, blank=True)
    DateTime_add        = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата и время обновления', auto_now=True)
    DescriptionWorks    = models.TextField(u'Что сделали', blank=True)
    DateTime_schedule   = models.DateField(u'Запланировано на:', null=True, blank=True)
    DateTime_work       = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    CoWorkers           = models.ManyToManyField(CoWorker, verbose_name='Исполнитель', blank=True)
    Status              = models.ForeignKey(Status, verbose_name='Статус заявки', default=2)
    def __str__(self):  return self.TypeSecurity
    class Meta:
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок '

class trouble_shooting(models.Model):
    AddressObject       = models.CharField(u'Адрес объекта', max_length=100)
    TypeSecurity        = models.ManyToManyField(TypeSecurity, verbose_name='Тип сигнализации', help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")
    Client_words        = models.CharField(u'Наименование', max_length=100)
    Routes              = models.ForeignKey(RoutesMaintenance,verbose_name='Маршрут', null=True, blank=True)
    Client_bd           = models.ForeignKey(Client,verbose_name='Контрагент', help_text="Обязательно для заполнения перед закрытием заявки", null=True, blank=True)
    Company             = models.ForeignKey(Company, verbose_name='Организация исполнитель')
    FaultAppearance     = models.TextField(u'Вид неисправности')
    DescriptionWorks    = models.TextField(u'Что сделали', blank=True)
    DateTime_work       = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    CoWorkers           = models.ManyToManyField(CoWorker, verbose_name='Исполнитель', blank=True)
    Status              = models.ForeignKey(Status, verbose_name='Статус заявки', default=2)
    DateTime_add        = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата и время обновления', auto_now=True)
    Create_user         = models.IntegerField(u'ID пользователя создавшего заявку')
    Update_user         = models.IntegerField(u'ID пользователя закрывшего заявку', null=True, blank=True)
    def __str__(self):  return self.NumObject
    class Meta:
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок '