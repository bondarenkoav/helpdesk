from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Menu(MPTTModel):
    name    = models.CharField('Название', max_length=50) #, unique=True)
    slug    = models.SlugField('Ключ категории')
    parent  = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель", related_name='child', db_index=True)
    icon    = models.CharField('Класс иконки bootstrap', max_length=10, help_text="Допустим: search")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = u'Ветка меню '
        verbose_name_plural = u'Дерево меню '
    class MPTTMeta:
        level_attr = 'mptt_level'
