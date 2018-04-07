import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from claim.models import support_request
from maintenance.models import objects_to, maintenance_request, Status_object, trouble_shooting
from maintenance.forms import request_maintenance_per_month, get_new_save_request, \
    request_status_filter, maintenance_object_status, get_add_trouble_shooting_form, get_add_object_to
from reference_books.models import ExpandedUserProfile, Status


@login_required
def get_requests_maintenance(request,status='open'):
    args = {}
    args.update(csrf(request))
    args['status'] = status_query = Status.objects.get(slug=status)

    form = request_status_filter(request.POST)

    if request.method == 'POST' and form.is_valid():
        change_month = request.POST['month_list']
        str_address  = request.POST['address']
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
        objects = objects_to.objects.filter(ServingCompany=user_company,AddressObject__icontains=str_address)
        args['requests'] = maintenance_request.objects.filter(Object=objects, Status=status_query.id, DateTime_schedule__month=change_month, DateTime_schedule__year=datetime.datetime.today().year)

    args['form'] = form

    return render(request, 'request_maintenance/request_list.html', args)


@login_required
def addget_request_maintenance(request, request_id=None, object_id=None):
    args = {}
    args.update(csrf(request))

    form = get_new_save_request(request.POST or None, instance=request_id and maintenance_request.objects.get(id=request_id))
    create_support_request = request.POST.get('create_support_request', False)

    if request.method == 'POST' and form.is_valid():
        new_request = form.save(commit=False)
        if request_id==None:
            new_request.Create_user = request.user.id
            new_request.Object = objects_to.objects.get(id=object_id)
        else:
            new_request.Update_user = request.user.id
        new_request.save()
        form.save_m2m()

        if create_support_request == 'on':
            request_data = maintenance_request.objects.get(id=request_id)
            support_request.objects.create(
                NumObject         = request_data.Object.NumObject,
                AddressObject     = request_data.Object.AddressObject,
                Client            = request_data.Object.Client.Name,
                Company           = request_data.Object.ServingCompany,
                Create_user       = request.user.id,
                FaultAppearance   = request_data.DescriptionWorks,
                DateTime_schedule = request_data.DateTime_work+datetime.timedelta(days=1)
            )
        return HttpResponseRedirect(reverse('maintenance:add&get_request',args=[new_request.Object.id,new_request.id]))
    else:
        args['form'] = form
        if request_id:
            args['request_data'] = maintenance_request.objects.get(id=request_id)
        else:
            args['object_data'] = objects_to.objects.get(id=object_id)

        return render(request, 'request_maintenance/request_item.html', args)


@login_required
def get_objects_maintenance(request):
    args = {}
    args.update(csrf(request))

    form = maintenance_object_status(request.POST)
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

    if request.method == 'POST' and form.is_valid():
        args['objects'] = objects_to.objects.filter(ServingCompany=user_company,Status=int(request.POST['object_status'])).order_by('Client')

    args['form'] = form
    return render(request, 'objects/object_list.html', args)


@login_required
def addget_object_maintenance(request, object_id=None):
    args = {}
    args.update(csrf(request))

    form = get_add_object_to(request.POST or None, user=request.user, instance=object_id and objects_to.objects.get(id=object_id))

    if request.method == 'POST' and form.is_valid():
        Company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

        new_object = form.save(commit=False)
        if object_id==None:
            new_object.Create_user = request.user.id
        else:
            new_object.Update_user = request.user.id
        new_object.Company = Company
        new_object.save()
        form.save_m2m()

        return HttpResponseRedirect(reverse('maintenance:add&get_object',args=[new_object.id]))
    else:
        args['form'] = form
        if object_id:
            args['object_data'] = objects_to.objects.get(id=object_id)

        return render(request, 'objects/object_item.html', args)


@login_required
def get_requests_maintenance_change_month(request):
    args = {}
    args.update(csrf(request))

    form = request_maintenance_per_month(request.POST)

    status_object = Status_object.objects.get(slug='open').id
    status_request = Status.objects.get(slug='open').id

    if request.POST and form.is_valid():
        change_month = int(request.POST['month_list'])
        routes = request.POST['routs']
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

        if change_month != '':
            if routes != '':
                list_objects = objects_to.objects.filter(ServingCompany=user_company,Routes=routes,Status=status_object) # Month_schedule=change_month
                args['trouble_shooting'] = trouble_shooting.objects.filter(Status=status_request,Routes=routes) # DateTime_add__year=datetime.datetime.today().year
            else:
                list_objects = objects_to.objects.filter(ServingCompany=user_company,Status=status_object)

            args['requests'] = maintenance_request.objects.filter(Object=list_objects,DateTime_add__month=change_month, DateTime_add__year=datetime.datetime.today().year)

    args['form'] = form
    return render(request, 'request_maintenance/request_permonth_list.html', args)


@login_required
def get_trouble_shooting(request, page_id=1):
    args = {}
    if page_id == None:
        page_id = 1
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
    status_query = Status.objects.get(slug='open')
    current_page = Paginator(trouble_shooting.objects.filter(Company=user_company,Status=status_query).order_by('-id'),50)
    args['requests'] = current_page.page(page_id)

    return render(request, 'trouble_shooting/trouble_list.html', args)


@login_required
def addget_trouble_shooting_item(request, request_id=None):
    args = {}
    args.update(csrf(request))

    form = get_add_trouble_shooting_form(request.POST or None, user=request.user, instance=request_id and trouble_shooting.objects.get(id=request_id))

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
        return HttpResponseRedirect(reverse('maintenance:get_troubles'))

    else:
        args['form'] = form
        if request_id:
            args['request_data'] = trouble_shooting.objects.get(id=request_id)

        return render(request, 'trouble_shooting/trouble_item.html', args)