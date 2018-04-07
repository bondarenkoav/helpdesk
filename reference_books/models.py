from django.contrib.auth.models import User, Group
from django.db import models



class City(models.Model):
    Name    = models.CharField(u'Город',max_length=100)
    slug    = models.SlugField(u'алиас')

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Город '
        verbose_name_plural = u'Список городов '


class Company(models.Model):
    Name    = models.CharField(u'Наименование', max_length=100)
    City    = models.ForeignKey(City, verbose_name='Город')
    slug    = models.SlugField(u'алиас', unique=True)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Сервисная компания '
        verbose_name_plural = u'Список сервисных компаний '


class ExpandedUserProfile(models.Model):
    Name            = models.CharField(u'ФИО пользователя', max_length=100)
    UserName        = models.ForeignKey(User, verbose_name='Имя пользователя')
    ServingCompany  = models.ForeignKey(Company, verbose_name='Сервисная компания')

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'ДопПрофиль пользователя '
        verbose_name_plural = u'Список профилей пользователей '


class Numerate(models.Model):
    ServingCompany  = models.ForeignKey(Company, verbose_name='Сервисная компания')
    slug_model      = models.SlugField(u'Название модели')
    last_num        = models.IntegerField(u'Последний номер')

    def __str__(self):  return self.slug_model
    class Meta:
        verbose_name = u'Счетчик '
        verbose_name_plural = u'Список счетчиков '


class Posts(models.Model):
    Name = models.CharField(u'Должность',max_length=100)
    slug = models.SlugField(u'алиас')

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Должность '
        verbose_name_plural = u'Список должностей '


class CoWorker(models.Model):
    Person_FIO      = models.CharField(u'ФИО сотрудника', max_length=100)
    Posts           = models.ForeignKey(Posts, verbose_name='Должность')
    ServingCompany  = models.ForeignKey(Company, verbose_name='Сервисная компания')
    StatusWorking   = models.BooleanField(u'Действующий сотрудник', default=True, help_text='Если сотрудник уволен, снимите галочку')

    def __str__(self):  return self.Person_FIO
    class Meta:
        verbose_name = u'Исполнитель '
        verbose_name_plural = u'Список исполнителей '


class Client(models.Model):
    Name = models.CharField(u'Контрагент', max_length=100)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Контрагент '
        verbose_name_plural = u'Список контрагентов '


class SystemPCN(models.Model):
    Name = models.CharField(u'Наименование ПЦН', max_length=50)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'ПЦН '
        verbose_name_plural = u'Список ПЦН '


class ModelTransmitter(models.Model):
    Name        = models.CharField(u'Модель передатчика', max_length=50)
    SystemPCN   = models.ForeignKey(SystemPCN, verbose_name='Наименование ПЦН')

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Модель передатчика'
        verbose_name_plural = u'Список моделей передатчиков '


class TypeSecurity(models.Model):
    Name        = models.CharField(u'Аббревиатура', max_length=10)
    Decription  = models.CharField(u'Полное наименование', max_length=100)
    slug        = models.SlugField(u'Алиас', max_length=50, unique=True)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Тип системы охраны '
        verbose_name_plural = u'Список системы охраны '


class Month_list(models.Model):
    Month_num  = models.CharField(u'Номер месяца', max_length=2)
    Month_name = models.CharField(u'Название месяца', max_length=50)

    def __str__(self):  return self.Month_name
    class Meta:
        verbose_name = u'Месяц '
        verbose_name_plural = u'Список месяцев '


class Send_mail_list(models.Model):
    GroupName      = models.CharField(u'Наименование группы получателей',max_length=100)
    ServingCompany = models.ForeignKey(Company,verbose_name='Сервисная компания')
    Subject        = models.CharField(u'Тема письма',max_length=100)
    Destination    = models.ManyToManyField(User, verbose_name='Получатели ', help_text='Выберите получателей уведомлений',max_length=2)
    Message        = models.TextField(u'Текст письма', help_text='В тексте письма обязательно должен находится тег %object%')
    EmailAddress   = models.EmailField(u'Электронный почтовый адрес')

    def __str__(self):  return self.GroupName
    class Meta:
        verbose_name = u'Получатель '
        verbose_name_plural = u'Список рассылки уведомлений '


class Status(models.Model):
    Name        = models.CharField(u'Состояние', max_length=100)
    slug        = models.SlugField(u'Ключ статуса', unique=True)
    tr_color    = models.CharField(u'Цвет строки', max_length=50)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Статус заявки '
        verbose_name_plural = u'Статусы заявок '


class Transmitter_serial(models.Model):
    Transmitter = models.ForeignKey(ModelTransmitter, verbose_name='Номер серийный устройства')
    Number = models.CharField(u'Модель устройства', max_length=50)

    def __str__(self):  return self.Transmitter.Name +' ('+ self.Number+')'
    class Meta:
        verbose_name = u'Серийный номер'
        verbose_name_plural = u'Список серйиных номеров устройств '


class RoutesMaintenance(models.Model):       # Маршруты (Номера маршрутов и описание)
    Number      = models.SmallIntegerField(u'Номер маршрута')
    Descript    = models.TextField(u'Описание маршрута', help_text='Введите последовательно населённые пункты данного маршрута')
    ServingCompany = models.ForeignKey(Company,verbose_name='Сервисная компания')
    #Locality = models.ManyToManyField(Settlements, verbose_name='Населённый пункт', help_text='Выберите населённые пункты входящие в маршрут')

    def __str__(self):  return self.Descript
    class Meta:
        verbose_name = u'Маршрут '
        verbose_name_plural = u'Список маршрутов ТО '


class OpSoS_name(models.Model):
    Name = models.CharField(u'Наименование', max_length=100, unique=True)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Сотовый оператор'
        verbose_name_plural = u'Список сотовых операторов '


class OpSoS_rate(models.Model):
    OpSoSName = models.ForeignKey(OpSoS_name, verbose_name='Сотовый оператор')
    Rate      = models.CharField(u'Наименование', max_length=100, unique=True)
    price     = models.DecimalField(u'Абонентская плата', max_digits=6, decimal_places=2, default=0)
    Descript  = models.TextField(u'Описание тарифа')

    def __str__(self):  return  str(self.OpSoSName)+' - '+self.Rate
    class Meta:
        verbose_name = u'Тариф '


class Event(models.Model):
    Name    = models.CharField(u'Наименование события', max_length=200, unique=True)
    slug    = models.SlugField(u'Алиас', max_length=100, unique=True)

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Событие '
        verbose_name_plural = u'События '