import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from urllib3.connectionpool import xrange

from accounts.views import get_cur_scompany
from exploitation.models import eproposals
from reference_books.models import CoWorker, Posts, Status
from report.forms import coworkers_range_date
from dashboard.models import logging


@login_required
@csrf_protect
def get_coworkers_range_date(request):
    form = coworkers_range_date(request.POST or None)

    if request.POST:
        if form.is_valid():

            dates = coworkers = list()

            user_company = get_cur_scompany(request.user)
            kind = form.cleaned_data['kind']
            date_start = form.cleaned_data['acts_date_start']
            date_end = form.cleaned_data['acts_date_stop']

            if kind == 'by_cowork':
                coworkers = CoWorker.objects.filter(ServiceCompany=user_company,
                                                    Posts__in=Posts.objects.filter(slug__in=['engineer', 'installer']),
                                                    StatusWorking=True).order_by('Person_FIO')
            else:
                date_range = date_end - date_start
                for days in xrange(date_range.days):
                    dates.append(date_start + timedelta(days))

            return render(request, 'employment_coworker.html', {
                'form': form,
                'kind': kind,
                'date_start': date_start,
                'date_end': date_end,
                'coworkers': coworkers,
                'dates': dates,
                'scompany': get_cur_scompany(request.user),
            })
    else:
        return render(request, 'employment_coworker.html', {
            'form': form
        })


@login_required
def get_jornal_changes(request, page_id=1):
    current_page = Paginator(logging.objects.all().order_by("-id"), 20)
    return render(request, 'jornal_change.html', {'jornal_changes': current_page.page(page_id)})


KANBAN_COLUMN = ["Принята", "Сегодня", "Завтра", "Исполнено", "Завершено"]


@login_required
def kanban(request):
    column_list = KANBAN_COLUMN
    all_tasks = []

    currdate = datetime.datetime.now().date()
    tomorrow = currdate + datetime.timedelta(days=1)
    if tomorrow.isoweekday() in [6, 7]:
        column_list[2] = "Понедельник"

    tasks = eproposals.objects.using('test').filter(ServiceCompany=get_cur_scompany(request.user))
    tasks_open = tasks.filter(Status=Status.objects.get(slug='open'))
    tasks_other = tasks.filter(Status__in=Status.objects.filter(slug__in=['complete', 'close']),
                               DateTime_work=datetime.datetime.now().date())
    tasks_union = tasks_open.union(tasks_other).order_by('-DateTime_add')

    for t in tasks_union:
        board_name = t.Status.Name

        if t.Status.slug == "open":
            if t.DateTime_schedule == currdate:
                board_name = "Сегодня"
            if tomorrow.isoweekday() in [6, 7]:
                delta = 7 - currdate.isoweekday() + 1
                next_monday = currdate + datetime.timedelta(days=delta)
                if t.DateTime_schedule == next_monday:
                    board_name = "Понедельник"
            elif t.DateTime_schedule == datetime.datetime.now().date()+datetime.timedelta(days=1):
                board_name = "Завтра"
        t_dict = {
            'uuid': t.pk,
            'client': t.Client_words,
            'name': t.NumObject + ' (' + t.AddressObject + ')',
            'descript': (t.DescriptionWorks if Status.slug in ['complete', 'close'] else t.FaultAppearance),
            'boardName': board_name,
            'date': (t.DateTime_schedule.strftime('%d.%m.%Y') if t.DateTime_schedule else 'не задан'),
            'url': reverse('exploitation:addget_eproposals', args=[t.pk])
        }
        all_tasks.append(t_dict)
    return render(request, 'kanban.html', {
        'column': column_list,
        'tasks': all_tasks,
    })
