import django_filters
from django.contrib.auth.models import User
from django.db import models
from django_currentuser.db.models import CurrentUserField

from reference_books.models import ServiceCompanies, OpSoS_name, OpSoS_rate, SystemPCN

USETYPESIM_CHOICES = (
    ('usesim_none', u'Не определено'),
    ('usesim_user', u'Корпоративная'),
    ('usesim_object', u'Объектовая'),
)


class OpSoS_card(models.Model):
    OpSoSRate = models.ForeignKey(OpSoS_rate, verbose_name='Тариф', max_length=100, on_delete=models.CASCADE)
    Number_SIM = models.CharField(u'Номер сим-карты', max_length=20)
    ICC_SIM = models.CharField(u'Ид.код сим-карты', max_length=25)
    Contract = models.CharField(u'Договор', max_length=100)
    ServiceCompany = models.ForeignKey(ServiceCompanies, verbose_name='Контрагент оператора', on_delete=models.CASCADE)
    Contract_date = models.DateField(u'Дата')
    PersonalAccount = models.CharField(u'Лицевой счёт', max_length=20)
    Use_type = models.CharField(u'Тип применения', choices=USETYPESIM_CHOICES, max_length=50, null=True, blank=True)
    SystemPCN = models.ForeignKey(SystemPCN, models.SET_NULL, null=True, verbose_name='ПЦН')
    Use_nameobject = models.CharField(u'Наименование объекта', max_length=300, blank=True)
    Use_numberobject = models.CharField(u'Номер объекта', max_length=30, blank=True)
    Use_addressobject = models.CharField(u'Адрес объекта', max_length=300, blank=True)
    Use_user = models.CharField(u'Фамилия Имя Отчество', max_length=100, blank=True)
    Notation = models.TextField(u'Примечание', null=True, blank=True)
    Status = models.BooleanField(u'SIM-карта активна', default=False)
    archive = models.BooleanField(u'Архив', default=False)

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='sim_create_user')
    Update_user = CurrentUserField(on_update=True, related_name='sim_update_user')

    def __str__(self):
        return self.Number_SIM.__str__()

    class Meta:
        app_label = 'sim'
        verbose_name = u'СИМ-карта '
        verbose_name_plural = u'Список сим-карт '
        permissions = (
            ('custom_add', u'Добавить SIM'),
            ('custom_view', u'Просмотреть SIM'),
            ('custom_change', u'Изменить SIM'),
            ('change_contract', u'поля.ДанныеДоговора'),
            ('change_sim', u'поля.ДанныеSIM'),
            ('change_usetype', u'поле.Применение'),
        )


class OpSoS_card_filter(django_filters.FilterSet):
    Status = django_filters.BooleanFilter(field_name='Status')
    ICC_SIM = django_filters.CharFilter(label=u'ID SIM', lookup_expr='icontains')
    Number_SIM = django_filters.CharFilter(label=u'Номер SIM', lookup_expr='icontains')
    Contract = django_filters.CharFilter(label=u'Договор', lookup_expr='icontains')
    Use_nameobject = django_filters.CharFilter(label='Имя объекта', lookup_expr='icontains')
    Use_numberobject = django_filters.CharFilter(label='Номер объекта', lookup_expr='icontains')
    Use_addressobject = django_filters.CharFilter(label='Адрес объекта', lookup_expr='icontains')
    Use_type = django_filters.ChoiceFilter(choices=USETYPESIM_CHOICES)
    Use_user = django_filters.CharFilter(label='ФИО сотрудника', lookup_expr='icontains')

    class Meta:
        model = OpSoS_card
        fields = ['Use_type']
