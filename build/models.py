from django.db import models

# Create your models here.
from reference_books.models import Client, TypeSecurity, Month_list, Company, CoWorker, ModelTransmitter, Status

class TypeRequest_build(models.Model):
    Name = models.CharField(u'Наименование', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Тип заявки '
        verbose_name_plural = u'Типы заявок '

class build_request(models.Model):
    Client              = models.ForeignKey(Client, verbose_name='Контрагент', max_length=100)
    AddressObject       = models.CharField(u'Адрес объекта', max_length=100)
    TypeRequest         = models.ForeignKey(TypeRequest_build, verbose_name='Тип монтажа')
    TypeSecurity        = models.ManyToManyField(TypeSecurity, verbose_name='Тип сигнализации', help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")
    Company             = models.ForeignKey(Company, verbose_name='Организация')
    Create_user         = models.IntegerField(u'ID пользователя создавшего заявку')
    Update_user         = models.IntegerField(u'ID пользователя закрывшего заявку', null=True, blank=True)
    DateTime_add        = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата и время обновления', auto_now=True)
    DescriptionWorks    = models.TextField(u'Подробное описание', blank=True)
    DateTime_schedule   = models.DateField(u'Запланировано на', null=True, blank=True)
    DateTime_work       = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    model_transmitter   = models.ForeignKey(ModelTransmitter, verbose_name='Модель передатчика', null=True, blank=True)
    num_transmitter     = models.CharField(u'Номер передатчика', max_length=15, null=True, blank=True)
    Status              = models.ForeignKey(Status, verbose_name='Статус заявки', default=2)
    def __str__(self):  return self.AddressObject
    class Meta:
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок '

class acts_build(models.Model):
    Name                = models.CharField(max_length=10,default='Акт')
    build_request       = models.ForeignKey(build_request, verbose_name='ID заявки на монтаж')
    Description         = models.TextField(u'Подробное описание', null=True, blank=True)
    Day_reporting       = models.DateField(u'Отчетный день')
    CoWorkers           = models.ManyToManyField(CoWorker, verbose_name='Исполнитель', blank=True)
    DateTime_add        = models.DateTimeField(u'Дата создания', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата обновления', auto_now=True)
    Create_user         = models.IntegerField(u'ID пользователя создавшего заявку')
    Update_user         = models.IntegerField(u'ID пользователя закрывшего заявку', null=True, blank=True)
    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Акт '
        verbose_name_plural = u'Список актов монтажа '