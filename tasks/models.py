# -*- coding: utf-8 -*-
import os
import django_filters

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.db import models
from ckeditor.fields import RichTextField
from django_currentuser.db.models import CurrentUserField

from accounts.models import Profile
from reference_books.models import Status_task, TypeNotification_task, CoWorker, TypeSecurity, ChannelsConnection, \
    MaterialsWorks, AdditionallyWorks, Status_calc


def validate_file_calculations(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Файл не поддерживается.')


def calculations_file_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "calculations_id%s.%s" % (str(instance.id), ext)
    return os.path.join('calculations/', filename)


Billing_TypeDocument = (
    ('contract', u'договор'),
    ('act', u'акт')
)


class Calculations(models.Model):
    # Оператор
    operator = models.ForeignKey(Profile, verbose_name=u'Оператор', related_name='prof_operator',
                                 help_text=u'Сотрудник принявший первый звонок от клиента', on_delete=models.CASCADE)
    DateTime_add = models.DateTimeField(u'Дата/время добавления задачи', auto_now_add=True)
    ContactPerson = models.CharField(u'Контактное лицо', max_length=100)
    TypeTask = models.ManyToManyField(TypeSecurity, verbose_name=u'Тип сигнализации')
    Description = models.TextField(u'Описание задачи', blank=True)
    AddressObject = models.CharField(u'Адрес объекта', max_length=300)
    NameObject = models.CharField(u'Наименование объекта', max_length=300, blank=True)
    Phone = models.CharField(u'Номер телефона', max_length=20, blank=True)
    Address_email = models.EmailField(u'Адрес эл.почты', blank=True)

    # Распорядитель
    disposer = models.ForeignKey(Profile, verbose_name=u'Распорядитель', related_name='prof_disposer', blank=True, null=True,
                                 help_text=u'Руководитель делегирующий роль исполнителя', on_delete=models.CASCADE)
    Disposer_DateTime_read = models.DateTimeField(u'Дата/время прочтения', blank=True, null=True)

    # Исполнитель
    executor = models.ForeignKey(Profile, verbose_name=u'Исполнитель', related_name='prof_executor', on_delete=models.CASCADE,
                                 blank=True, null=True, help_text=u'Ведёт клиента от "звонка" до "договора"')
    Executor_DateTime_read = models.DateTimeField(u'Дата/время прочтения', blank=True, null=True)
    DateTime_inspection_object = models.DateTimeField(u'Дата/время осмотра объекта', blank=True, null=True)
    Channels_connection = models.ManyToManyField(ChannelsConnection, verbose_name=u'Канал связи', blank=True)
    Frequency_tests = models.CharField(u'Периодичность тестов', max_length=50, blank=True)
    Date_build = models.DateTimeField(u'Дата и время начала работ', blank=True, null=True)
    Workorder = models.BooleanField(u'Выдан заказ-наряд', default=False)
    Workorder_num = models.IntegerField(u'Номер заказ-наряда', default=False, null=True)
    Abundance_materials = models.BooleanField(u'Материалов достаточно', default=False)

    # Менеджеры
    manager = models.ForeignKey(Profile, verbose_name=u'Менеджер', related_name='prof_manager', blank=True, null=True,
                                on_delete=models.CASCADE)
    Manager_DateTime_read = models.DateTimeField(u'Дата/время прочтения', blank=True, null=True)
    Estimate = models.FileField(u'Калькуляция', blank=True, null=True, validators=[validate_file_calculations],
                                upload_to=calculations_file_rename, help_text=u'Обязательно! Заверенная подписью клиента')
    Outlay = models.FileField(u'Смета', blank=True, null=True, validators=[validate_file_calculations],
                              upload_to=calculations_file_rename)
    Act_Delivery = models.FileField(u'Акт приёмо-сдачи', blank=True, null=True, validators=[validate_file_calculations],
                                    upload_to=calculations_file_rename,
                                    help_text=u'Не обязательно. Заверенная подписью клиента')
    Billing_TypeDocument = models.CharField(u'Тип документа в Биллинге', choices=Billing_TypeDocument, max_length=30,
                                            blank=True, null=True)
    Billing_NumDocument = models.IntegerField(u'ID договора монтажа в Биллинг', blank=True, null=True)

    # Бухгалтерия
    accountant = models.ForeignKey(Profile, verbose_name=u'Бухгалтер', related_name='prof_accountant', blank=True,
                                   null=True, on_delete=models.CASCADE)
    Accountant_DateTime_read = models.DateTimeField(u'Дата/время прочтения', blank=True, null=True)

    # Склад
    storekeeper = models.ForeignKey(Profile, verbose_name=u'Бухгалтер-материалист', related_name='prof_storekeeper',
                                    blank=True, null=True, on_delete=models.CASCADE)
    Store_DateTime_read = models.DateTimeField(u'Дата/время прочтения', blank=True, null=True)
    Date_waiting = models.DateField(u'Дата ожидаемого поступления материала', blank=True, null=True)
    Date_actual = models.DateField(u'Дата фактического поступления материала', blank=True, null=True)

    # Калькуляция
    commissioning = models.ForeignKey(AdditionallyWorks, verbose_name=u'Пуско-наладочные работы',
                                      related_name='aw1', blank=True, null=True, on_delete=models.CASCADE)
    projects = models.ForeignKey(AdditionallyWorks, verbose_name=u'Проектные работы', related_name='aw2',
                                 blank=True, null=True, on_delete=models.CASCADE)
    Sale = models.IntegerField(u'Процентное снижение', default=0, help_text=u'Применимо только к стоимости работ',
                               blank=True, null=True)
    client_consent = models.BooleanField(u'Получено согласие клиента', default=False, blank=True)
    total_summ = models.DecimalField(u'Итоговая стоимость', max_digits=10, decimal_places=2, default=0)

    Status = models.ForeignKey(Status_calc, models.SET_NULL, verbose_name='Статус', default=2, null=True)

    def __str__(self):
        return self.AddressObject

    class Meta:
        verbose_name = u'Калькуляция '
        verbose_name_plural = u'Калькуляции '
        permissions = (
            ('calc_list_view', u'Калькуляция. Просмотр списка'),
            ('calc_item_view', u'Калькуляция. Просмотр записи'),
            ('calc_item_add', u'Калькуляция. Добавление записи'),
            ('calc_item_edit', u'Калькуляция. Редактирование записи'),
        )


class CalcNotify(models.Model):
    calculation = models.ForeignKey(Calculations, verbose_name=u'Калькуляция', on_delete=models.CASCADE)
    title = models.CharField(u'Заголовок задачи', max_length=100)
    group_executor = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True, verbose_name=u'Группа исполнителей')
    executor = models.ForeignKey(Profile, models.SET_NULL, blank=True, null=True, verbose_name=u'Исполнитель')
    read = models.BooleanField(u'Прочтено',  blank=True, default=False)
    date_read = models.DateTimeField(u'Дата исполнения', blank=True, null=True)

    Create_user = CurrentUserField(on_update=False, related_name='tcn_creator')
    DateTime_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Уведомление '
        verbose_name_plural = u'Список уведомлений '


# Материалы
class CalcMaterialsWorks(models.Model):
    calculation = models.ForeignKey(Calculations, verbose_name=u'Калькуляция', on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialsWorks, verbose_name=u'Материал', on_delete=models.CASCADE)

    material_price = models.DecimalField(u'Стоимость материала', max_digits=7, decimal_places=2, default=0)
    material_rent = models.BooleanField(u'Аренда', default=False)
    work_price = models.DecimalField(u'Стоимость работ', max_digits=7, decimal_places=2, default=0)

    quantity = models.IntegerField(u'Количество', default=0)
    material_total = models.DecimalField(u'Итого материал', max_digits=7, decimal_places=2, default=0)

    work_total = models.DecimalField(u'Итого работа', max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return self.material.name

    class Meta:
        verbose_name = u'Материалы '
        verbose_name_plural = u'Список материалов '


# История
class CalcHistory(models.Model):
    calculation = models.ForeignKey(Calculations, verbose_name=u'Калькуляция', on_delete=models.CASCADE)
    event = models.CharField(u'Событие', max_length=300)
    value = models.CharField(u'Значение', max_length=300, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)

    def __str__(self):
        return self.event

    class Meta:
        verbose_name = u'Работы '
        verbose_name_plural = u'Список работ '
        permissions = (
            ('task_list_view', u'Работы. Просмотр списка'),
            ('task_item_view', u'Работы. Просмотр записи'),
            ('task_item_add', u'Работы. Добавление записи'),
            ('task_item_edit', u'Работы. Редактирование записи'),
        )


class TemplateDocuments(models.Model):  # Шаблоны договоров
    NameTemplate = models.CharField(u'Наименование шаблона', max_length=100)
    slug = models.SlugField(u'Алиас', max_length=100, unique=True)
    TextTemplate = RichTextField(u'Текст шаблона')

    def __str__(self):
        return self.NameTemplate

    class Meta:
        verbose_name = u'Шаблон '
        verbose_name_plural = u'Шаблоны документов '


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Файл не поддерживается.')


def task_file_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "task_id%s.%s" % (str(instance.id), ext)
    return os.path.join('tasks/', filename)


class user_task(models.Model):
    title = models.CharField(u'Заголовок задачи', max_length=100)
    description = models.TextField(u'Описание задачи')
    author = models.ForeignKey(User, verbose_name=u'Назначающий', related_name='author', on_delete=models.CASCADE)
    group_executor = models.ForeignKey(Group, models.SET_NULL, null=True, verbose_name=u'Группа исполнителей')
    executor = models.ForeignKey(Profile, models.SET_NULL, null=True, verbose_name=u'Исполнитель', related_name='executor')
    client = models.CharField(u'Контрагент', max_length=100, blank=True, null=True)

    Date_limit = models.DateField(u'Дата исполнения', blank=True, null=True)
    high_importance = models.BooleanField(u'Высокая важность', default=False)
    notification = models.ForeignKey(TypeNotification_task, models.SET_NULL, null=True,
                                     verbose_name=u'Способ уведомления о статусе заявки')
    status = models.ForeignKey(Status_task, models.SET_NULL, null=True, verbose_name=u'Статус выполнения')
    work_desc = models.TextField(u'Описание выполнения', blank=True, null=True)
    read = models.BooleanField(u'Прочтено', default=False)
    file = models.FileField(blank=True, null=True, validators=[validate_file_extension], upload_to=task_file_rename)

    Create_user = CurrentUserField(on_update=False, related_name='ut_creator')
    Update_user = CurrentUserField(on_update=True, related_name='ut_modifying')

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Задача '
        verbose_name_plural = u'Список задач '
        permissions = (
            ('task_list_view', u'Задачи. Просмотр списка'),
            ('task_item_view', u'Задачи. Просмотр записи'),
            ('task_item_add', u'Задачи. Добавление записи'),
            ('task_item_edit', u'Задачи. Редактирование записи'),
        )


class tasks_filter(django_filters.FilterSet):
    executor = django_filters.ModelChoiceFilter(label=u'Исполнитель', queryset=Profile.objects.all())

    class Meta:
        model = user_task
        fields = ['executor', 'client']
