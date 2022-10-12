from django.db import models
from django_currentuser.db.models import CurrentUserField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from reference_books.models import TypeDocument, ServiceCompanies, TypeRequest, Event


class Menu(MPTTModel):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('Ключ категории')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель",
                            related_name='child', db_index=True,  on_delete=models.CASCADE)
    icon = models.CharField('Класс иконки bootstrap', max_length=10, help_text="Допустим: search", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Ветка меню '
        verbose_name_plural = u'Дерево меню '

    class MPTTMeta:
        level_attr = 'mptt_level'


# choices=(('request', u'заявка'), ('object', u'объект'), ('act', u'акт'), ('route', u'маршрут'),)


class logging(models.Model):
    app = models.ForeignKey(TypeRequest, models.SET_NULL, null=True, verbose_name='Приложение')
    type_dct = models.CharField(u'Тип документа', blank=True, max_length=50)
    dct_id = models.IntegerField(u'Идентификатор документа', blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.CASCADE)
    old_value = models.CharField(u'Старое значение', max_length=300, blank=True, null=True)

    add_date = models.DateTimeField(u'Дата и время записи', auto_now_add=True)
    user = CurrentUserField(on_update=False, related_name='user_event_add')

    def __str__(self):
        return self.app.short_name

    class Meta:
        verbose_name = u'Событие '
        verbose_name_plural = u'Журнал событий '
