import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf
from build.forms import get_new_save_acts_build, coworkers_range_date, coworkers_object, coworker_range_date, get_new_save_request
from build.models import acts_build, build_request
from dashboard.views import custom_proc
from reference_books.models import ExpandedUserProfile, CoWorker, Status


@login_required
def get_requests_build(request,status='open'):
    args = {}
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
    args['status'] = status_query = Status.objects.get(slug=status)
    if status=='complete':
        args['requests'] = build_request.objects.filter(Company=user_company,Status=status_query.id,DateTime_add__year=datetime.datetime.today().year).order_by('-id')
    else:
        args['requests'] = build_request.objects.filter(Company=user_company,Status=status_query.id).order_by('-id')

    return render(request, 'request_build/request_list.html', args)


@login_required
def addget_request_build(request, request_id=None):
    args = {}
    args.update(csrf(request))

    form = get_new_save_request(request.POST or None, instance=request_id and build_request.objects.get(id=request_id))

    if request.method == 'POST' and form.is_valid():
        Company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
        item = form.save(commit=False)
        if request_id==None:
            item.Create_user = request.user.id
        else:
            item.Update_user = request.user.id
        item.Company = Company
        item.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('build:get_requests',args=['open']))

    else:
        args['form'] = form
        if request_id:
            args['request_data'] = build_request.objects.get(id=request_id)
            args['list_acts'] = acts_build.objects.filter(build_request=request_id)

        return render(request, 'request_build/request_item.html', args)


@login_required
def get_acts_build(request,page_id=1):
    list_acts = acts_build.objects.all()
    current_page = Paginator(list_acts,20)
    return render(request, 'acts/act_list.html', {'acts': current_page.page(page_id)})


@login_required
def addget_act_build(request, request_id=None, act_id=None):
    args = {}
    args.update(csrf(request))

    form = get_new_save_acts_build(request.POST or None, user=request.user, instance=act_id and acts_build.objects.get(id=act_id))

    if request.method == 'POST' and form.is_valid():
        new_request = form.save(commit=False)
        if act_id==None:
            new_request.Create_user = request.user.id
        else:
            new_request.Update_user = request.user.id
        new_request.build_request = build_request.objects.get(id=request_id)
        new_request.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('build:add&get_request', args=[request_id]))

    else:
        args['form'] = form
        if act_id:
            args['act_data'] = acts_build.objects.get(id=act_id)
        else:
            args['request_data'] = build_request.objects.get(id=request_id)
        return render(request, 'acts/act_item.html', args)


@login_required
def get_coworkers_range_date(request):
    args = {}
    args.update(csrf(request))

    form = coworkers_range_date(request.POST)
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

    if request.method == 'POST' and form.is_valid():
        acts_date_start = datetime.date(int(request.POST['acts_date_start_year']), int(request.POST['acts_date_start_month']), int(request.POST['acts_date_start_day']))
        acts_date_stop  = datetime.date(int(request.POST['acts_date_stop_year']), int(request.POST['acts_date_stop_month']), int(request.POST['acts_date_stop_day']))

        args['acts_date_start'] = acts_date_start
        args['acts_date_stop'] = acts_date_stop

        if acts_date_start != '' and acts_date_stop != '':
            args['coworkers'] = CoWorker.objects.filter(ServingCompany=user_company).order_by('Person_FIO')
            args['list_works'] = acts_build.objects.filter(Day_reporting__range=(acts_date_start, acts_date_stop))

        args['form'] = coworkers_range_date

        return render(request, 'employment_coworker.html', args)


@login_required
def get_coworker_range_date(request):
    args = {}
    args.update(csrf(request))

    form = coworker_range_date(request.POST, user=request.user)

    if request.method == 'POST' and form.is_valid():
        coworker        = request.POST['CoWorkers']
        no_range_date   = request.POST.get('no_range_date', False)
        acts_date_start = datetime.date(int(request.POST['acts_date_start_year']), int(request.POST['acts_date_start_month']), int(request.POST['acts_date_start_day']))
        acts_date_stop  = datetime.date(int(request.POST['acts_date_stop_year']), int(request.POST['acts_date_stop_month']), int(request.POST['acts_date_stop_day']))

        args['acts_date_start'] = acts_date_start
        args['acts_date_stop'] = acts_date_stop

        if no_range_date != 'on' and coworker != '':
            if acts_date_start != ''and acts_date_stop != '' and coworker != '':
                args['acts'] = acts_build.objects.filter(CoWorkers=coworker,Day_reporting__range=(acts_date_start, acts_date_stop))
                args['request'] = acts_build.objects.filter(CoWorkers=coworker,Day_reporting__range=(acts_date_start, acts_date_stop)).distinct(build_request)
            else:
                args['acts_participation'] = acts_build.objects.filter(CoWorkers=coworker)#.order_by(support_request)
                args['acts_edited'] = acts_build.objects.filter(CoWorkers=coworker)#.order_by(support_request)
    else:
        args['form'] = coworker_range_date
        return render(request, 'coworker_range_date.html', args)


@login_required
def get_coworkers_object(request):
    args = {}
    args.update(csrf(request))

    form = coworkers_object(request.POST, user=request.user)

    if request.method == 'POST' and form.is_valid():
        num_request_build = request.POST['support_request']

        if num_request_build != '':
            args['request']     = build_request.objects.get(id=num_request_build)
            list_acts           = acts_build.objects.filter(support_request=num_request_build).order_by('Day_reporting')
            args['list_acts']   = list_acts
            args['build_day']   = list_acts.count()
            args['build_start'] = list_acts.first()
            args['build_stop']   = list_acts.last()
            args['request_build'] = build_request.objects.get(id=num_request_build)
    else:
        args['form'] = coworkers_object

        return render(request, 'coworkers_object.html', args)