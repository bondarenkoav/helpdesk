# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from reference_books.models import ServiceCompanies, Posts, City

GENDER_CHOICES = (
    ('man', u'Мужской'),
    ('woman', u'Женский')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scompany = models.ManyToManyField(ServiceCompanies, related_name='scompany_select',
                                      verbose_name=u'Сервисные компании (доступные)',
                                      help_text='Выбрать сервисные компании доступные пользователю')
    scompany_default = models.ForeignKey(ServiceCompanies, models.SET_NULL, related_name='scompany_default',
                                         verbose_name=u'Сервисная компания (по умолчанию)', null=True, blank=True)
    scompany_current = models.ForeignKey(ServiceCompanies, models.SET_NULL, related_name='scompany_current',
                                         verbose_name=u'Сервисные компании (текущая)', null=True, blank=True)
    location = models.ForeignKey(City, models.SET_NULL, verbose_name=u'Место нахождения', null=True, blank=True)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone = models.CharField(u'Номер телефона', blank=True, max_length=10,
                             help_text=u'Вводить номер в федеральном формате, без кода страны 8 или +7')
    gender = models.CharField(u'Пол', choices=GENDER_CHOICES, max_length=50, blank=True)
    personal_data = models.BooleanField(u'Согласие на обработку персональных данных', default=False)
    viewlist = models.BooleanField(u'Отображать в списках на выбор', default=False)

    class Meta:
        ordering = ["user__last_name"]

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    # Обновление поля "сервисная компания по умолчанию"
#    try:
#        obj_profile = Profile.objects.get(user=instance)
# Если компании у пользователя выбраны, хотя бы одна
#        if obj_profile.scompany.all().count() > 0:
# Если поле "сервисная компания по умолчанию" пустое или не входит в список доступных компаний
#            if obj_profile.scompany_default == None:
#                Profile.objects.filter(user=instance).update(scompany_default=obj_profile.scompany.first())
# if obj_profile.scompany.filter():
#    Profile.objects.filter(user=instance).update(scompany_default=obj_profile.scompany.first())
# Если не выбраны, то нужно очистить оба поля
#        else:
# Profile.objects.filter(user=instance).update(scompany_default=None, scompany_current=None)
#    except:
#        pass
