# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from reference_books.models import ServiceCompanies, Posts


# class Sections(models.Model):
#     name = models.CharField(u'Раздел', max_length=30)
#     slug = models.SlugField(u'Алиас')
#
#     def __str__(self):  return self.name
#
# class Fields(models.Model):
#     section = models.ForeignKey(Sections, verbose_name=u'Секция')
#     name    = models.CharField(u'Поле', max_length=100)
#     slug    = models.SlugField(u'Алиас')
#
#     def __str__(self):  return self.name
#
#
# class GroupSettings(models.Model):
#     group     = models.ManyToManyField(Group)
#     section   = models.ForeignKey(Sections, verbose_name=u'Секция')
#     item_add  = models.BooleanField(u'Добавить',default=True)
#     item_view = models.BooleanField(u'Просмотр',default=True)
#     item_upd  = models.BooleanField(u'Обновить',default=True)
#
#     def __str__(self):  return self.section_fields.section.name+'.'+self.section_fields.name
#     class Meta:
#         verbose_name = u'Параметр '
#         verbose_name_plural = u'Список параметров групп '
#
# @receiver(post_save, sender=Group)
# def create_or_update_group_profile(sender, instance, created, **kwargs):
#     if created:
#         GroupSettings.objects.create(group=instance)
#     #instance.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scompany = models.ManyToManyField(ServiceCompanies, verbose_name=u'Сервисные компании', help_text='Выбрать сервисные компании доступные пользователю')
    location = models.CharField(u'Место нахождения', max_length=50, blank=True)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone    = models.CharField(u'Номер телефона', blank=True, max_length=10, help_text=u'Вводить номер в федеральном формате, без кода страны 8 или +7')
    personal_data = models.BooleanField(u'Согласие на обработку персональных данных', default=False)

    def __str__(self):  return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# class UsersSettings(models.Model):
#     custom_profile  = models.ForeignKey(Profile, verbose_name=u'Профиль пользователя')
#     section_fields  = models.ForeignKey(Fields, verbose_name=u'Секция.Поле')
#     section_add     = models.BooleanField(u'Установить',default=True)
#     section_upd     = models.BooleanField(u'Обновить',default=True)
#
#     def __str__(self):  return self.section_fields.section.name+'.'+self.section_fields.name
#     class Meta:
#         verbose_name = u'Параметр '
#         verbose_name_plural = u'Список исключений '