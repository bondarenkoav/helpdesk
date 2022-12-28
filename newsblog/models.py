from django.db import models
from django.contrib.auth.models import User, Group
from django_currentuser.db.models import CurrentUserField

from accounts.models import Profile


class PostUpdate(models.Model):
    title = models.CharField(u'Заголовок', max_length=200, unique=True)
    target_group = models.ManyToManyField(Group, verbose_name=u'Целевая группа')
    author = models.ForeignKey(Profile, verbose_name=u'Автор', on_delete=models.CASCADE)
    content = models.TextField()
    public = models.BooleanField(u'Опубликовано', default=True)

    DateTime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    DateTime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    Create_user = CurrentUserField(on_update=False, related_name='nbpu_creator')
    Update_user = CurrentUserField(on_update=True, related_name='nbpu_modifying')

    class Meta:
        verbose_name = u'Пост '
        verbose_name_plural = u'Посты обновлений программы '
        ordering = ['-DateTime_add']

    def __str__(self):
        return self.title
