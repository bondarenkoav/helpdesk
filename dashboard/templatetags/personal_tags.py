import math

from datetime import datetime
from django.db.models import Q
from django import template
from django.contrib.auth.models import User

from tasks.models import user_task, CalcNotify
from accounts.models import Profile
from reference_books.models import CoWorker, Status, Status_task
from build.models import bacts, bproposals


__author__ = 'ipman'
register = template.Library()


@register.filter
def view_shortfio_user(user):
    try:
        return get_shortfio(user.last_name+' '+user.first_name)
    except:
        return 'ошибка'


@register.filter
def view_shortfio_user(login):
    try:
        user = User.objects.get(username=login)
        return get_shortfio(user.last_name+' '+user.first_name)
    except:
        return 'ошибка'


@register.filter
def get_gender(user):
    try:
        return Profile.objects.get(user=user).gender
    except:
        return 'ошибка'


@register.filter
def view_shortfio_coworker(coworker_id):
    if coworker_id:
        return get_shortfio(CoWorker.objects.get(id=coworker_id).Person_FIO)
    else:
        return 'ошибка'


@register.filter
def get_shortfio(fio):
    if fio:
        split_fio = fio.split(' ')
        if len(split_fio) == 1:
            return split_fio
        elif len(split_fio) == 2:
            return split_fio[0]+' '+split_fio[1][:1]+'.'
        elif len(split_fio) == 3:
            return split_fio[0]+' '+split_fio[1][:1]+'.'+split_fio[2][:1]+'.'
        else:
            return 'неизвестно'
    else:
        return 'нет'


@register.inclusion_tag('templatetags/notify.html')
def notify_topbar(user_data):
    tasks = user_task.objects.filter(Q(author=user_data, status__in=Status_task.objects.filter(slug='complete'))|
                                     Q(executor=Profile.objects.get(user=user_data))|
                                     Q(group_executor__in=user_data.groups.all()),
                                     status__in=Status_task.objects.exclude(slug__in=['complete', 'canceled']),
                                     read=False)
    notify = CalcNotify.objects.\
        filter(Q(executor=Profile.objects.get(user=user_data))|Q(group_executor__in=user_data.groups.all()), read=False)
    count_notify = tasks.count() + notify.count()
    return {'tasks': tasks, 'notify': notify, 'count_notify': count_notify, 'cur_date': datetime.today().date()}


@register.filter
def get_coworkers_build(value):
    list_cowork = ''
    req = bproposals.objects.get(id=int(value))
    acts = bacts.objects.filter(build_request=req)
    for act in acts:
        for cowork in act.CoWorkers.all():
            full_name = cowork.Person_FIO.split(' ')
            if full_name[0] != '' and full_name[1] != '':
                name_short = full_name[0]+' '+full_name[1][:1]+'.'
            else:
                name_short = full_name[0]
            if list_cowork.find(name_short)==-1:
                if list_cowork != '':
                    list_cowork = list_cowork+', '+name_short
                else:
                    list_cowork = name_short
    return list_cowork


@register.filter
def get_status_name(value):
    return Status.objects.get(slug=value).Name


# Определяем: Юбиляр или именинник
@register.simple_tag()
def get_jubilee(birthday_year):
    try:
        if math.fmod(datetime.today().year - birthday_year, 5) == 0:
            return True
        else:
            return False
    except ArithmeticError:
        return False


# Проверить на принадлежность к группе
@register.simple_tag()
def check_user_in_group(username, groupname):
    current_user = User.objects.get(username=username)
    if bool(current_user.groups.filter(name=groupname)):
        return 'yes'
    else:
        return 'no'
