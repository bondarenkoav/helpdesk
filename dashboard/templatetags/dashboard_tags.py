import random
from datetime import datetime, timedelta
from django import template
from django.template.defaultfilters import stringfilter

from accounts.models import Profile
from accounts.views import get_cur_scompany
from build.models import bproposals
from dashboard.views import get_activeusers
from exploitation.models import eproposals
from dashboard.models import Menu
from maintenance.models import mproposals, mobjects, count_completeproposals_per_month
from reference_books.models import Status, CoWorker, Month_list
from helpdesk.settings import *
from accounts.forms import change_cur_scompany_form
from sim.models import OpSoS_card

__author__ = 'ipman'
register = template.Library()


@register.inclusion_tag('templatetags/new_function.html')
def new_function():
    title = 'Новая функция! (режим тестирования)'
    text = '<p>АРМ Заявки пополнился новой функцией - Задачи. Поставить и ' \
           'проконтролировать исполнение задачи стало проще, достаточно кликнуть по иконке уведомлений (возле меню ' \
           'пользователя) и нажать "Смотреть все", затем "+" в правом верхнем углу.</p>' \
           '<p>Все новые задания Вы можете увидеть нажав на иконку уведомлений и просмотреть список или пройти по ссылке "Смотреть все".</p>' \
           '<p>Уведомление о выполненой задаче может быть: внутрисистемное, отправлено по смс или же на эл. почту.</p>' \
           '<p>Обновление от 14.06.2019! Теперь автор может приложить файл к задаче. ' \
           'Просмотр файла возможен на всем протяжении "жизни" задачи: автором и исполнителем. ' \
           'Удаление или изменение файла невозможно в случаях:</p>' \
           '<ul><li>У задачи статус: "Исполнено".</li><li>Файл желает изменить/удалить не автор задачи</li></ul>'
    return {'title': title, 'text': text}


@register.inclusion_tag('templatetags/user_active.html')
def informer_usersactive():
    return {'users': get_activeusers()}


@register.inclusion_tag('templatetags/user_birthdayboy.html')
def informer_birthdayboy():
    lastname = Profile.objects.filter(birthday__day=datetime.today().day,
                                      birthday__month=datetime.today().month)

    return {'birthdayboy': Profile.objects.filter(birthday__day=datetime.today().day,
                                                  birthday__month=datetime.today().month),
            'image_url': 'img/present_%d.png' % random.randrange(1, 4, 1)}


@register.simple_tag()
def get_completrequest_engineers(cowork_id, day):
    count_eproposals = eproposals.objects.filter(
        Status=Status.objects.get(slug='close'),
        CoWorkers=CoWorker.objects.get(id=cowork_id),
        DateTime_work=day
    ).count()
    count_mproposals = mproposals.objects.filter(
        Status=Status.objects.get(slug='close'),
        CoWorkers=CoWorker.objects.get(id=cowork_id),
        DateTime_work=day
    ).count()
    return count_eproposals + count_mproposals


@register.simple_tag()
def get_completrequest_maintenace(year, month):
    cp = count_completeproposals_per_month.objects.filter(dmonth=month, dyear=str(round(year)))
    if cp:
        return cp.first().id
    else:
        return 0


@register.inclusion_tag('templatetags/informer_exploitation.html')
def informer_exploitation(user):
    list_coworker = CoWorker.objects.filter(ServiceCompany=get_cur_scompany(user))
    proposals_all = eproposals.objects.filter(ServiceCompany=get_cur_scompany(user))
    proposals_open = proposals_all.filter(Status=Status.objects.get(slug='open'),
                                          CoWorkers__isnull=True).count()
    proposals_work = proposals_all.filter(Status=Status.objects.get(slug='open'),
                                          CoWorkers__in=list_coworker).count()
    proposals_control = proposals_all.filter(Status=Status.objects.get(slug='control')).count()
    return {'proposals_open': proposals_open, 'proposals_work': proposals_work, 'proposals_control': proposals_control}


@register.inclusion_tag('templatetags/informer_build.html')
def informer_build(user):
    proposals_all = bproposals.objects.filter(ServiceCompany=get_cur_scompany(user))
    proposals_open = proposals_all.filter(Status=Status.objects.get(slug='open')).count()
    proposals_today = proposals_all.filter(Status=Status.objects.get(slug='open'),
                                           DateTime_schedule=datetime.today()).count()
    proposals_control = proposals_all.filter(Status=Status.objects.get(slug='control')).count()
    return {'proposals_open': proposals_open, 'proposals_today': proposals_today, 'proposals_control': proposals_control}


@register.inclusion_tag('templatetags/informer_maintenance.html')
def informer_maintenance(user):
    list_objects = mobjects.objects.filter(ServiceCompany=get_cur_scompany(user))

    proposals_curmonth = mproposals.objects.filter(Object__in=list_objects,
                                                   DateTime_schedule__month=datetime.now().month,
                                                   DateTime_schedule__year=datetime.now().year)
    proposals_open = proposals_curmonth.filter(Status=Status.objects.get(slug='open'), CoWorkers__isnull=True).count()
    proposals_work = proposals_curmonth.filter(Status=Status.objects.get(slug='open'), CoWorkers__isnull=False).count()
    proposals_control = proposals_curmonth.filter(Status=Status.objects.get(slug='control')).count()
    return {'proposals_open': proposals_open, 'proposals_work': proposals_work, 'proposals_control': proposals_control}


@register.inclusion_tag('templatetags/informer_sim.html')
def informer_sim(user):
    list_sim_work = OpSoS_card.objects.filter(Status=True,ServiceCompany=get_cur_scompany(user)).order_by('id')
    list_sim_corp = list_sim_work.filter(Use_type='usesim_user').count()
    list_sim_obj = list_sim_work.filter(Use_type='usesim_object').count()
    return {'list_sim_work': list_sim_work.count(), 'list_sim_corp': list_sim_corp, 'list_sim_obj': list_sim_obj}


@register.inclusion_tag('templatetags/topbar.html')
def tag_topbar(user):
    return {'user': user, 'form': change_cur_scompany_form(user=user)}


@register.inclusion_tag('templatetags/topbar_mobile.html')
def tag_topbar_mobile(user):
    return {'user': user}


@register.inclusion_tag('templatetags/navigation.html')
def tag_navigation():
    return {'nodes':Menu.objects.all()}


@register.filter
@stringfilter
def get_constans(value):
    if value == 'dev_name':
        return DEVELOP_NAME
    elif value == 'dev_email':
        return DEVELOP_EMAIL
    elif value == 'owner':
        return OWNER


@register.simple_tag()
def get_namemonth(month):
    return Month_list.objects.get(Month_num=str(round(month)))


@register.simple_tag()
def get_count_options_filter(mydict):
    i = 0
    list_values = dict(mydict.list()).values()
    for option in list_values:
        len_option = len(option.pop())
        if len_option > 0:
            i = i + 1
    return i


@register.filter
def plus_days(value, days):
    return value + timedelta(days=days)


@register.filter
def minus_days(value, days):
    return value - timedelta(days=days)
