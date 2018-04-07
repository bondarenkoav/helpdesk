from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.db import models
from reference_books.models import Company, CoWorker, ModelTransmitter, TypeSecurity, Status, Client

class CategoryMenu(MPTTModel):
    name    = models.CharField('Название', max_length=50) #, unique=True)
    slug    = models.SlugField('Ключ категории')
    parent  = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель", related_name='child', db_index=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = u'Ветка меню '
        verbose_name_plural = u'Дерево меню '
    class MPTTMeta:
        level_attr = 'mptt_level'


class TypeRequest(models.Model):
    Name = models.CharField(u'Наименование', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Тип заявки '
        verbose_name_plural = u'Типы заявок '


class support_request(models.Model):
    NumObject           = models.CharField(u'№ объекта',max_length=10)
    model_transmitter   = models.ForeignKey(ModelTransmitter, verbose_name='Модель передатчика', null=True, blank=True)
    num_transmitter     = models.CharField(u'Номер передатчика', max_length=15, null=True, blank=True)
    AddressObject       = models.CharField(u'Адрес объекта', max_length=100)
    TypeSecurity        = models.ManyToManyField(TypeSecurity, verbose_name='Тип сигнализации', help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")
    Client_bd           = models.ForeignKey(Client,verbose_name='Контрагент', help_text="Обязательно для заполнения перед закрытием заявки", null=True, blank=True)
    Client              = models.CharField(u'Наименование', max_length=100)
    Company             = models.ForeignKey(Company, verbose_name='Организация')
    Create_user         = models.IntegerField(u'ID пользователя создавшего заявку')
    Update_user         = models.IntegerField(u'ID пользователя закрывшего заявку', null=True, blank=True)
    DateTime_add        = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата и время обновления', auto_now=True)
    FaultAppearance     = models.TextField(u'Вид неисправности')
    DescriptionWorks    = models.TextField(u'Что сделали', blank=True)
    DateTime_schedule   = models.DateField(u'Запланировано на:', null=True, blank=True)
    DateTime_work       = models.DateField(u'Дата и время исполнения', null=True, blank=True)
    CoWorkers           = models.ManyToManyField(CoWorker, verbose_name='Исполнитель', blank=True)
    Status              = models.ForeignKey(Status, verbose_name='Статус заявки', default=2)
    Required_act        = models.BooleanField(u'Требуется акт выполненных работ', default=False)
    Date_act            = models.DateField(u'Дата предоставления акта', null=True, blank=True)

    def __str__(self):  return self.NumObject
    class Meta:
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок '