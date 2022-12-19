import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from urllib3.connectionpool import xrange
from django.http import JsonResponse

from accounts.views import get_cur_scompany
from exploitation.models import eproposals
from reference_books.models import CoWorker, Posts, Status
from report.forms import coworkers_range_date
from dashboard.models import logging
from django.utils.formats import localize


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


KANBAN_COLUMN = [
    {'label': "Принято", 'id': "open"},
    {'label': "Сегодня", 'id': "today"},
    {'label': "Завтра", 'id': "tomorrow"},
    {'label': "Исполнено", 'id': "complete"},
    {'label': "Завершено", 'id': "close"},
]


@login_required
def kanban(request):
    all_tasks = []
    t_list = eproposals.objects.filter(
        ServiceCompany=get_cur_scompany(request.user),
        DateTime_schedule__lte=datetime.datetime.today(),
        Status__in=Status.objects.filter(slug__in=['open']))
    for t in t_list:
        t_dict = {
            'id': str(t.id),
            'name': t.NumObject + "(" + t.AddressObject + ")",
            'boardName': 'Принята',
            'date': t.DateTime_add
        }
        all_tasks.append(t_dict)
    return render(request, 'kanban.html', {'tasks': all_tasks})

    # proposals = eproposals.objects.\
    #     filter(ServiceCompany=get_cur_scompany(request.user), DateTime_schedule__lte=datetime.datetime.today()).\
    #     exclude(Status__in=Status.objects.filter(slug__in=['scheduled', 'transfer', 'not_fulfilled', 'control']))
    # output = []
    # for query in proposals:
    #     # output.append('id': query.id, 'name': query.name, etc...)
    #     var = output.append[
    #           'label': query.DescriptionWorks, 'priority': 1, 'color': "#58C3FE",
    #           'start_date': query.DateTime_add.strftime('%m/%d/%Y'), 'users': [3, 1], 'column': "open", 'type': "task"]
    # return render(request, 'kanban.html', {'data': proposals})
