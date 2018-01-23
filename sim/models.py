from django.db import models
from reference_books.models import Company, OpSoS_name, OpSoS_rate, SystemPCN


class UseTypeSIM(models.Model):
    Name = models.CharField(u'Название', max_length=100)
    slug = models.SlugField(u'алиас')

    def __str__(self):  return self.Name
    class Meta:
        verbose_name = u'Тип '
        verbose_name_plural = u'Типы применения SIM-карт '


class OpSoS_card(models.Model):
    OpSoSRate           = models.ForeignKey(OpSoS_rate,verbose_name='Тариф',max_length=100)
    Number_SIM          = models.CharField(u'Номер сим-карты', max_length=20)
    ICC_SIM             = models.CharField(u'Ид.код сим-карты', max_length=22)
    Contract            = models.CharField(u'Договор', max_length=100)
    Owner               = models.ForeignKey(Company, verbose_name='Контрагент оператора')
    Contract_date       = models.DateField(u'Дата')
    PersonalAccount     = models.IntegerField(u'Лицевой счёт')
    Use_type            = models.ForeignKey(UseTypeSIM, verbose_name='Тип применения')
    SystemPCN           = models.ForeignKey(SystemPCN, verbose_name='ПЦН')
    Use_nameobject      = models.CharField(u'Наименование объекта',max_length=300, blank=True)
    Use_numberobject    = models.CharField(u'Номер объекта',max_length=30, blank=True)
    Use_addressobject   = models.CharField(u'Адрес объекта',max_length=300, blank=True)
    Use_user            = models.CharField(u'Фамилия Имя Отчество', max_length=100, blank=True)
    Notation            = models.TextField(u'Примечание', null=True, blank=True)
    Status              = models.BooleanField(u'SIM-карта активна', default=True)
    DateTime_add        = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update     = models.DateTimeField(u'Дата и время обновления', auto_now=True)
    Create_user         = models.IntegerField(u'ID пользователя создавшего запись')
    Update_user         = models.IntegerField(u'ID пользователя изменившего запись', null=True, blank=True)

    def __str__(self):  return str(self.Number_SIM)
    class Meta:
        verbose_name = u'СИМ-карта '
        verbose_name_plural = u'Список сим-карт '