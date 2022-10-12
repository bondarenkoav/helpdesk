from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from urllib3.connectionpool import xrange

from accounts.views import get_cur_scompany
from reference_books.models import CoWorker, Posts
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
