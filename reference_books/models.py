from autoslug import AutoSlugField
from django.contrib.auth.models import User, Group
from django.db import models


CITYTYPE_CHOICES = (
    ('г', u'город'),
    ('пгт', u'посёлок городского типа'),
    ('п', u'посёлок'),
    ('д', u'деревня'),
    ('с', u'село'),
)


class City(models.Model):
    Name = models.CharField(u'Населённый пункт', max_length=100)
    TypeCity = models.CharField(u'Тип',  choices=CITYTYPE_CHOICES, max_length=20)

    def __str__(self):
        return self.TypeCity + ' ' + self.Name

    class Meta:
        verbose_name = u'Населённый пункт '
        verbose_name_plural = u'Список населённых пунктов '


class TypeRequest(models.Model):
    Name = models.CharField(u'Наименование', max_length=100)
    short_name = models.CharField(u'Аббревиатура', max_length=10)
    slug = models.SlugField(u'Ключ статуса', unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Тип заявки '
        verbose_name_plural = u'Типы заявок '


class TypeDocument(models.Model):
    Name = models.CharField(u'Наименование', max_length=100)
    short_name = models.CharField(u'Аббревиатура', max_length=10)
    slug = models.SlugField(u'Ключ статуса', unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Тип документа '
        verbose_name_plural = u'Типы документов '


class TypeBuild(models.Model):
    Name = models.CharField(u'Наименование', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Тип '
        verbose_name_plural = u'Типы работ '


class ServiceCompanies(models.Model):
    Name = models.CharField(u'Наименование', max_length=100)
    City = models.ForeignKey(City, models.SET_NULL, verbose_name=u'Город', null=True)
    slug = models.SlugField(u'алиас', unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Сервисная компания '
        verbose_name_plural = u'Список сервисных компаний '


class TypesClient(models.Model):  # Типы клиентов: ИП, Физлицо, Юрлицо
    short_name = models.CharField(u'Абревиатура', max_length=30)
    slug = models.SlugField(u'Алиас', unique=True)
    full_name = models.TextField(u'Подробное описание')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = u'Тип контрагентов '
        verbose_name_plural = u'Типы контрагентов '


class Client(models.Model):
    TypesClient = models.ForeignKey(TypesClient, verbose_name=u'Тип клиента', on_delete=models.CASCADE)
    Name = models.CharField(u'Контрагент', max_length=100)
    INN = models.CharField(u'ИНН', max_length=12)
    KPP = models.CharField(u'КПП', max_length=9, blank=True)
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name=u'Сервисная компания', on_delete=models.CASCADE)

    def __str__(self):
        return self.TypesClient.short_name + ' ' + self.Name + ' (' + self.INN + '/' + self.KPP + ')'

    class Meta:
        ordering = ['Name']
        verbose_name = u'Контрагент '
        verbose_name_plural = u'Список контрагентов '


class Numerate(models.Model):
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name=u'Сервисная компания', on_delete=models.CASCADE)
    slug_model = models.SlugField(u'Название модели')
    last_num = models.IntegerField(u'Последний номер')

    def __str__(self):
        return self.slug_model

    class Meta:
        verbose_name = u'Счетчик '
        verbose_name_plural = u'Список счетчиков '


class Posts(models.Model):
    Name = models.CharField(u'Должность', max_length=100)
    slug = models.SlugField(u'алиас')

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Должность '
        verbose_name_plural = u'Список должностей '


class CoWorker(models.Model):
    Person_FIO = models.CharField(u'ФИО сотрудника', max_length=100)
    Posts = models.ForeignKey(Posts, models.SET_NULL, verbose_name=u'Должность', null=True)
    location = models.CharField(u'Местонахождение', max_length=50)
    ServiceCompany = models.ManyToManyField(ServiceCompanies, verbose_name=u'Сервисная компания',
                                            help_text=u'Для выделения нескольких компаний, удерживать клавишу Ctrl')
    Username = models.ForeignKey(User, models.SET_NULL, verbose_name=u'Пользователь', blank=True, null=True)
    StatusWorking = models.BooleanField(u'Действующий сотрудник', default=True,
                                        help_text=u'Если сотрудник уволен, снимите галочку')

    def __str__(self):
        split_fio = self.Person_FIO.split(' ')
        if len(split_fio) == 1:
            return split_fio + ' (' + self.location + ')'
        elif len(split_fio) == 2:
            return split_fio[0] + ' ' + split_fio[1][:1] + '.' + ' (' + self.location + ')'
        elif len(split_fio) == 3:
            return split_fio[0] + ' ' + split_fio[1][:1] + '.' + split_fio[2][:1] + '.' + ' (' + self.location + ')'
        else:
            return 'неизвестно'

    class Meta:
        ordering = ['Person_FIO']
        verbose_name = u'Исполнитель '
        verbose_name_plural = u'Список исполнителей '


class SystemPCN(models.Model):
    Name = models.CharField(u'Наименование ПЦН', max_length=50)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'ПЦН '
        verbose_name_plural = u'Список ПЦН '


class ModelTransmitter(models.Model):
    Name = models.CharField(u'Модель передатчика', max_length=50)
    SystemPCN = models.ForeignKey(SystemPCN, models.SET_NULL, verbose_name=u'Наименование ПЦН', null=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Модель передатчика'
        verbose_name_plural = u'Список моделей передатчиков '


class TypeSecurity(models.Model):
    Name = models.CharField(u'Аббревиатура', max_length=10)
    Decription = models.CharField(u'Полное наименование', max_length=100)
    slug = models.SlugField(u'Алиас', max_length=50, unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Тип системы охраны '
        verbose_name_plural = u'Список системы охраны '


class Month_list(models.Model):
    Month_num = models.CharField(u'Номер месяца', max_length=2)
    Month_name = models.CharField(u'Название месяца', max_length=50)

    def __str__(self):
        return self.Month_name

    class Meta:
        ordering = ['id']
        verbose_name = u'Месяц '
        verbose_name_plural = u'Список месяцев '


class Send_mail_list(models.Model):
    GroupName = models.CharField(u'Наименование группы получателей', max_length=100)
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name=u'Сервисная компания', on_delete=models.CASCADE)
    Subject = models.CharField(u'Тема письма', max_length=100)
    Destination = models.ManyToManyField(User, verbose_name='Получатели ',
                                         help_text=u'Выберите получателей уведомлений', max_length=2)
    Message = models.TextField(u'Текст письма', help_text=u'В тексте письма обязательно должен находится тег %object%')
    EmailAddress = models.EmailField(u'Электронный почтовый адрес')

    def __str__(self):
        return self.GroupName

    class Meta:
        verbose_name = u'Получатель '
        verbose_name_plural = u'Список рассылки уведомлений '


class Status(models.Model):
    Name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    view_form = models.BooleanField(u'Отображать в форме')
    returneq_form = models.BooleanField(u'Отображать в форме "Возврат оборудования"')
    tr_color = models.CharField(u'Цвет строки', max_length=50)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Статус заявки '
        verbose_name_plural = u'Статусы заявок '


class Status_task(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    class_b4 = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True,
                                help_text=u'Классы: active, primary, secondary, success, '
                                          u'danger, warning, info, light, dark')
    view_list = models.BooleanField(u'Выводить в список', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы задач '


class Status_calc(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    class_b4 = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True,
                                help_text=u'Классы: active, primary, secondary, success, '
                                          u'danger, warning, info, light, dark')
    view_list = models.BooleanField(u'Выводить в список', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы калькуляции '


class TypeNotification_task(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    color = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип '
        verbose_name_plural = u'Варианты уведомления '


class Transmitter_serial(models.Model):
    Transmitter = models.ForeignKey(ModelTransmitter, verbose_name=u'Номер серийный устройства', on_delete=models.CASCADE)
    Number = models.CharField(u'Модель устройства', max_length=50)

    def __str__(self):
        return self.Transmitter.Name + ' (' + self.Number + ')'

    class Meta:
        verbose_name = u'Серийный номер'
        verbose_name_plural = u'Список серйиных номеров устройств '


class RoutesMaintenance(models.Model):  # Маршруты (Номера маршрутов и описание)
    Number = models.SmallIntegerField(u'Номер маршрута')
    Descript = models.TextField(u'Описание маршрута',
                                help_text=u'Введите последовательно населённые пункты данного маршрута')
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name=u'Сервисная компания', on_delete=models.CASCADE)

    def __str__(self):
        return self.Descript.__str__()

    class Meta:
        ordering = ['Descript']
        verbose_name = u'Маршрут '
        verbose_name_plural = u'Список маршрутов ТО '


class OpSoS_name(models.Model):
    Name = models.CharField(u'Наименование', max_length=100, unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Сотовый оператор'
        verbose_name_plural = u'Список сотовых операторов '


class OpSoS_rate(models.Model):
    OpSoSName = models.ForeignKey(OpSoS_name, verbose_name=u'Сотовый оператор', on_delete=models.CASCADE)
    Rate = models.CharField(u'Наименование', max_length=250, unique=True)
    price = models.DecimalField(u'Абонентская плата', max_digits=6, decimal_places=2, default=0)
    Descript = models.TextField(u'Описание тарифа')

    def __str__(self):
        return str(self.OpSoSName) + ' - ' + self.Rate

    class Meta:
        verbose_name = u'Тариф '


class Event(models.Model):
    Name = models.CharField(u'Наименование события', max_length=200, unique=True)
    slug = models.SlugField(u'Алиас', max_length=100, unique=True)
    template = models.TextField(u'Шаблон', blank=True, null=True, help_text='Заполнять не обязательно')
    forfilter = models.BooleanField(u'Фильтр', default=False, blank=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Событие '
        verbose_name_plural = u'События '


# Каналы передачи данных
class ChannelsConnection(models.Model):
    Name = models.CharField(u'Наименование события', max_length=100, unique=True)
    slug = models.SlugField(u'Алиас', max_length=100, unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = u'Канал '
        verbose_name_plural = u'Каналы связи '


# Единицы измерения
class Measure(models.Model):
    name = models.CharField(u'Наименование', max_length=100, unique=True)
    shortname = models.CharField(u'Абревиатура', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Единица измерения '
        verbose_name_plural = u'Единицы измерения '


# Наборы оборудования
class SetMaterials(models.Model):
    name = models.CharField(u'Наименование', max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Набор '
        verbose_name_plural = u'Наборы материалов '


# Материалы
class MaterialsWorks(models.Model):
    name = models.CharField(u'Наименование', max_length=300)
    set = models.ManyToManyField(SetMaterials, verbose_name=u'Набор', related_name='set_materials')
    model = models.CharField(u'Модель', max_length=100)
    measure = models.ForeignKey(Measure, verbose_name=u'Единица измерения',
                                max_length=100, on_delete=models.CASCADE)
    rent_set = models.ManyToManyField(SetMaterials, verbose_name=u'В аренду для набора',
                                      related_name='rent_set_materials')
    material_price = models.DecimalField(u'Стоимость оборуд/материала', max_digits=7, decimal_places=2)
    work_price = models.DecimalField(u'Стоимость работ', max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return self.name + ' (' + str(self.model) + ')'

    class Meta:
        verbose_name = u'Материал '
        verbose_name_plural = u'Материалы и работы '


# Дополнительные виды работ
class AdditionallyWorks(models.Model):
    name = models.CharField(u'Наименование', max_length=300)
    price = models.DecimalField(u'Стоимость работ', max_digits=7, decimal_places=2, default=0)
    type = models.CharField(u'Тип работ', choices=(('commissioning', 'пуско-наладка'), ('projects', 'проект')),
                            max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Работа '
        verbose_name_plural = u'Дополнительные виды работы '
