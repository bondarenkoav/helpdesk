import datetime
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.template.context_processors import csrf
from claim.models import support_request
from claim.views import custom_proc
from maintenance.models import objects_to, maintenance_request, Status_object, trouble_shooting
from maintenance.forms import request_maintenance_per_month, get_new_save_request, \
    request_status_filter, maintenance_object_status, get_add_trouble_shooting_form, get_add_object_to
from reference_books.models import ExpandedUserProfile, Status, TypeSecurity, Company, Client


def get_requests_maintenance(request,status='open',page_id=1):
    args = {}
    #user = get_object_or_404(User, pk=request.user.id)

    if request.user.is_active:
        #if user.has_perm('claim.change_bar') == True:
        args.update(csrf(request))
        form = request_status_filter(request.POST)

        if request.POST:
            change_month = request.POST['month_list']
            str_address  = request.POST['address']
            user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
            status_query = Status.objects.get(slug=status).id

            if form.is_valid():
                objects = objects_to.objects.filter(ServingCompany=user_company,AddressObject__icontains=str_address)
                args['requests'] = maintenance_request.objects.filter(Object=objects,Status=status_query,DateTime_schedule__month=change_month)

        args['status'] = Status.objects.get(slug=status)
        args['form'] = request_status_filter

        return render_to_response('request_maintenance/requests_status.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_new_save_request_item(request, request_id=None, object_id=None):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        formset = get_new_save_request(request.POST or None, instance=request_id and maintenance_request.objects.get(id=request_id))
        create_support_request = request.POST.get('create_support_request', False)

        if request.method == 'POST' and formset.is_valid():
            item = formset.save(commit=False)

            if request_id==None:
                item.Create_user = request.user.id
                item.Object = objects_to.objects.get(id=object_id)
            else:
                item.Update_user = request.user.id
            item.save()
            formset.save_m2m()

            if create_support_request == 'on':
                request_data = maintenance_request.objects.get(id=request_id)
                client_id = request_data.Object.Client.id

                p = support_request(
                    NumObject         = request_data.Object.NumObject,
                    AddressObject     = request_data.Object.AddressObject,
                    #TypeSecurity      = request_data.Object.TypeSecurity,
                    Client            = request_data.Object.Client.Name,
                    #Client_db         = Client.objects.get(id=client_id),
                    Company           = request_data.Object.ServingCompany,
                    Create_user       = request.user.id,
                    FaultAppearance   = request_data.DescriptionWorks,
                    DateTime_schedule = request_data.DateTime_work+datetime.timedelta(days=1)
                )
                p.save(force_insert=True)

            return HttpResponseRedirect('/')

        args['form'] = formset
        args['client'] = objects_to.objects.get(id=object_id).Client
        args['address'] = objects_to.objects.get(id=object_id).AddressObject
        args['num_object'] = objects_to.objects.get(id=object_id).NumObject
        args['request_id'] = request_id
        args['object_id'] = object_id

        return render_to_response('request_maintenance/request_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_objects_to_status(request):
    args = {}
    if request.user.is_active:
        args.update(csrf(request))
        form = maintenance_object_status(request.POST)

        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

        if request.POST:
            object_status = int(request.POST['object_status'])

            if form.is_valid():
                args['list_object'] = objects_to.objects.filter(ServingCompany=user_company,Status=object_status).order_by('Client')
                #current_page = Paginator(objects_to.objects.filter(ServingCompany=user_company,Status=object_status).order_by('Client'),20)

        args['form'] = maintenance_object_status

        return render_to_response('objects/objects_status.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_add_object_to_item(request, object_id=None):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))
        formset = get_add_object_to(request.POST or None, user=request.user, instance=object_id and objects_to.objects.get(id=object_id))

        if request.method == 'POST' and formset.is_valid():
            Company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

            item = formset.save(commit=False)
            if object_id==None:
                item.Create_user = request.user.id
            else:
                item.Update_user = request.user.id
            item.Company = Company
            item.save()
            formset.save_m2m()

            return HttpResponseRedirect('/maintenance/objects/')

        args['form'] = formset
        args['object_id'] = object_id

        return render_to_response('objects/object_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_requestTO_change_month(request):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))
        form = request_maintenance_per_month(request.POST)

        status_object = Status_object.objects.get(slug='open').id
        status_request = Status.objects.get(slug='open').id

        if request.POST and form.is_valid():
            change_month = request.POST['month_list']
            routes = request.POST['routs']
            user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

            if change_month != '':
                if routes != '':
                    list_objects = objects_to.objects.filter(ServingCompany=user_company,Month_schedule=change_month,Routes=routes,Status=status_object)
                    args['trouble_shooting'] = trouble_shooting.objects.filter(Status=status_request,Routes=routes)
                else:
                    list_objects = objects_to.objects.filter(ServingCompany=user_company,Month_schedule=change_month,Status=status_object)
                args['requests'] = maintenance_request.objects.filter(Status=status_request,Object=list_objects)

        args['form'] = form
        return render_to_response('objects/objects_per_month.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_trouble_shooting(request, page_id=1):
    args = {}

    if request.user.is_active:
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
        status_query = Status.objects.get(slug='open')
        current_page = Paginator(trouble_shooting.objects.filter(Company=user_company,Status=status_query).order_by('-id'),20)
        args['requests'] = current_page.page(page_id)

        return render_to_response('trouble_shooting/trouble_shooting.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_add_trouble_shooting_item(request, request_id=None):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        formset = get_add_trouble_shooting_form(request.POST or None, user=request.user, instance=request_id and trouble_shooting.objects.get(id=request_id))

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

            return HttpResponseRedirect('/maintenance/trouble_shooting/')

        args['form'] = formset
        args['request_id'] = request_id

        return render_to_response('trouble_shooting/trouble_shooting_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')