import datetime
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.template.context_processors import csrf
from build.forms import get_new_save_acts_build, coworkers_range_date, coworkers_object, coworker_range_date, get_new_save_request
from build.models import acts_build, build_request
from claim.views import custom_proc
from reference_books.models import ExpandedUserProfile, CoWorker, Status

def get_requests_build(request,status='open',page_id=1):
    args = {}

    if request.user.is_active:
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
        status_query = Status.objects.get(slug=status)
        #status_query = Status.objects.get(slug='open')
        current_page = Paginator(build_request.objects.filter(Company=user_company,Status=status_query.id).order_by('-id'),20)
        args['requests'] = current_page.page(page_id)
        args['status'] = status_query

        return render_to_response('request_build/requests_status.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_new_save_request_build_item(request, request_id=None):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        formset = get_new_save_request(request.POST or None, instance=request_id and build_request.objects.get(id=request_id))

        if request.method == 'POST' and formset.is_valid():
            Company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

            item = formset.save(commit=False)
            if request_id==None:
                item.Create_user = request.user.id
            else:
                item.Update_user = request.user.id
            item.Company = Company
            item.save()
            formset.save_m2m()
            return HttpResponseRedirect('/build/open/')

        args['form'] = formset
        args['request_id'] = request_id

        if request_id!=None:
            args['status'] = build_request.objects.get(id=request_id).Status.slug
            args['list_acts'] = acts_build.objects.filter(build_request=request_id)

        return render_to_response('request_build/request_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_acts_build(request,page_id=1):

    if request.user.is_active:
        list_acts = acts_build.objects.all()
        current_page = Paginator(list_acts,20)
        return render_to_response('acts/acts_all.html', {'acts': current_page.page(page_id)}, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_new_save_acts_build_item(request, request_id=None, act_id=None):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        formset = get_new_save_acts_build(request.POST or None, user=request.user, instance=act_id and acts_build.objects.get(id=act_id))
        request_query = build_request.objects.get(id=request_id)

        args['form'] = formset
        args['act_id'] = act_id
        args['request_id'] = request_id

        if request.method == 'POST' and formset.is_valid():

            #if acts_build.objects.filter(build_request=request_id).count() == 0:        #
            item = formset.save(commit=False)
            if act_id==None:
                item.Create_user = request.user.id
            else:
                item.Update_user = request.user.id
            item.build_request = request_query
            item.save()
            formset.save_m2m()

            return HttpResponseRedirect('/build/item/'+str(request_id)+'/')
            #else:
            #    args['error'] = 'Акт на этот объект и дату уже внесен!'
            #    return render_to_response('acts/acts_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))

        return render_to_response('acts/acts_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_coworkers_range_date(request):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))
        form = coworkers_range_date(request.POST)
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

        if request.POST:
            acts_date_start = datetime.date(int(request.POST['acts_date_start_year']), int(request.POST['acts_date_start_month']), int(request.POST['acts_date_start_day']))
            acts_date_stop  = datetime.date(int(request.POST['acts_date_stop_year']), int(request.POST['acts_date_stop_month']), int(request.POST['acts_date_stop_day']))

            args['acts_date_start'] = acts_date_start
            args['acts_date_stop'] = acts_date_stop

            if form.is_valid():
                if acts_date_start != '' and acts_date_stop != '':
                    args['coworkers'] = CoWorker.objects.filter(ServingCompany=user_company).order_by('Person_FIO')
                    args['list_works'] = acts_build.objects.filter(Day_reporting__range=(acts_date_start, acts_date_stop))

        args['form'] = coworkers_range_date

        return render_to_response('report/coworkers_range_date.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_coworker_range_date(request):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        form = coworker_range_date(request.POST, user=request.user)

        if request.POST:
            coworker        = request.POST['CoWorkers']
            no_range_date   = request.POST.get('no_range_date', False)
            acts_date_start = datetime.date(int(request.POST['acts_date_start_year']), int(request.POST['acts_date_start_month']), int(request.POST['acts_date_start_day']))
            acts_date_stop  = datetime.date(int(request.POST['acts_date_stop_year']), int(request.POST['acts_date_stop_month']), int(request.POST['acts_date_stop_day']))

            args['acts_date_start'] = acts_date_start
            args['acts_date_stop'] = acts_date_stop

            if form.is_valid():
                if no_range_date != 'on' and coworker != '':
                    if acts_date_start != ''and acts_date_stop != '' and coworker != '':
                        args['acts'] = acts_build.objects.filter(CoWorkers=coworker,Day_reporting__range=(acts_date_start, acts_date_stop))
                        args['request'] = acts_build.objects.filter(CoWorkers=coworker,Day_reporting__range=(acts_date_start, acts_date_stop)).distinct(build_request)
                else:
                    args['acts_participation'] = acts_build.objects.filter(CoWorkers=coworker)#.order_by(support_request)
                    args['acts_edited'] = acts_build.objects.filter(CoWorkers=coworker)#.order_by(support_request)
                    acts = acts_build.objects.filter(CoWorkers=coworker).distinct(build_request)

        args['form'] = coworker_range_date

        return render_to_response('report/coworker_range_date.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_coworkers_object(request):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        form = coworkers_object(request.POST, user=request.user)

        if request.POST:
            num_request_build = request.POST['support_request']

            if form.is_valid():
                if num_request_build != '':
                    #a = acts_build.objects.filter(support_request=num_request_build).prefetch_related('CoWorkers')
                    args['request']     = build_request.objects.get(id=num_request_build)
                    list_acts           = acts_build.objects.filter(support_request=num_request_build).order_by('Day_reporting')
                    args['list_acts']   = list_acts
                    args['build_day']   = list_acts.count()
                    args['build_start'] = list_acts.first()
                    args['build_stop']   = list_acts.last()
                    args['request_build'] = build_request.objects.get(id=num_request_build)

        args['form'] = coworkers_object

        return render_to_response('report/coworkers_object.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')