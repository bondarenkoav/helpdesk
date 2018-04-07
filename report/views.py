import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from build.models import build_request
from claim.models import support_request
from claim.views import custom_proc
from maintenance.models import maintenance_request, objects_to
from reference_books.models import ExpandedUserProfile, CoWorker, Status
from report.forms import coworkers_range_date
from report.models import logging
from django.contrib.auth.decorators import login_required


@login_required
def get_coworkers_range_date(request):
    args = {}
    args.update(csrf(request))
    form = coworkers_range_date(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
            args['date_start'] = datetime.datetime.strptime(request.POST['acts_date_start'], "%d.%m.%Y").date()
            args['date_end'] = datetime.datetime.strptime(request.POST['acts_date_stop'], "%d.%m.%Y").date()
            args['coworkers'] = CoWorker.objects.filter(ServingCompany=user_company,StatusWorking=True).order_by('Person_FIO')

    args['form'] = coworkers_range_date
    return render(request, 'employment_coworker.html', args)


def logging_event(code_event, user_data, old_value='', app='base'):
    logging.objects.create(application=app, event_code=code_event, old_value=old_value, user=user_data)


@login_required
def get_jornal_changes(request,page_id=1):
    current_page = Paginator(logging.objects.all().order_by("-id"),20)
    return render(request, 'jornal_change.html', {'jornal_changes':current_page.page(page_id)})