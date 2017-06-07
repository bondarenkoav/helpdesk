import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from build.models import acts_build
from claim.models import support_request
from claim.views import custom_proc
from maintenance.models import maintenance_request
from reference_books.models import ExpandedUserProfile, CoWorker, Status
from report.forms import coworkers_range_date
from report.models import logging


def get_coworkers_range_date(request):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))
        form = coworkers_range_date(request.POST)
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

        if request.POST:
            acts_date_start = datetime.datetime.strptime(request.POST['acts_date_start'], "%d.%m.%Y").date()
            acts_date_stop  = datetime.datetime.strptime(request.POST['acts_date_stop'], "%d.%m.%Y").date()

            args['acts_date_start'] = acts_date_start
            args['acts_date_stop'] = acts_date_stop

            status_id = Status.objects.get(slug='complete').id

            if form.is_valid():
                if acts_date_start != '' and acts_date_stop != '':
                    args['coworkers'] = CoWorker.objects.filter(ServingCompany=user_company).order_by('Person_FIO')
                    args['list_build'] = acts_build.objects.filter(Day_reporting__range=(acts_date_start, acts_date_stop))
                    args['list_claim'] = support_request.objects.filter(DateTime_work__range=(acts_date_start, acts_date_stop),Status=status_id)
                    args['list_maintenance'] = maintenance_request.objects.filter(DateTime_work__range=(acts_date_start, acts_date_stop),Status=status_id)

        args['form'] = coworkers_range_date

        return render_to_response('report/coworkers_range_date.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')


def logging_event(code_event, user_data, old_value='', app='base'):
    logging.objects.create(application=app, event_code=code_event, old_value=old_value, user=user_data)


def get_jornal_changes(request,page_id=1):
    args = {}

    if request.user.is_active:
        current_page = Paginator(logging.objects.all().order_by("-id"),20)
        args['jornal_changes'] = current_page.page(page_id)

        return render_to_response('jornal_change.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')