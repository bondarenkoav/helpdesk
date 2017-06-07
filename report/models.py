from django.contrib.auth.models import User
from django.db import models
from reference_books.models import Event


class logging(models.Model):
    application = models.SlugField(u'Приложение', max_length=30)
    event_code  = models.ForeignKey(Event, verbose_name='Событие')
    old_value   = models.CharField(u'Старое значение', max_length=100, blank=True, null=True)
    add_date    = models.DateTimeField(u'Дата и время записи', auto_now_add=True)
    user        = models.ForeignKey(User, verbose_name='Пользователь')
    def __str__(self):  return self.application
    class Meta:
        verbose_name = u'Событие '
        verbose_name_plural = u'Журнал событий '
