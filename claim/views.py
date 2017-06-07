import datetime
#from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.context_processors import csrf
from claim.models import support_request, CategoryMenu
from claim.forms import get_new_save_request, LoginForm, request_per_date
from reference_books.models import ExpandedUserProfile, Status

def log_in(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponseRedirect('/')
    else:
        args['form'] = LoginForm()
    return render_to_response('login.html', args)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

# def date_convert(s):
#     return datetime.strptime(s, "%d.%m.%Y").strftime('%Y,%m,%d')

def get_user_perms(request):
    user = get_object_or_404(User, pk=request.user.id)
    return {
        'add'    : user.has_perm('claim.add_bar'),
        'change' : user.has_perm('claim.change_bar'),
        'delete' : user.has_perm('claim.delete_bar'),
    }

def custom_proc(request):
    return {
        'nodes'             : CategoryMenu.objects.all(),
        'app'               : 'АРМ "Заявки"',
        'owner'             : 'Группа предприятий "Амулет"',
        'user'              : request.user,
        'developer_name'    : 'Бондаренко А.В.',
        'developer_email'   : 'printex.orsk@gmail.com',
        'user_group'        : request.user.groups.values('name'),
    }

def get_requests_trouble_shooting(request,status='open',page_id=1):
    args = {}

    if request.user.is_active:
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
        status_query = Status.objects.get(slug=status)
        current_page = Paginator(support_request.objects.filter(Company=user_company,Status=status_query.id).order_by('-id'),20)
        args['requests'] = current_page.page(page_id)
        args['status'] = status_query

        return render_to_response('request_trouble_shooting/requests_status.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_requests_per_date(request):
    args = {}

    if request.user.is_active:
        args.update(csrf(request))
        form = request_per_date(request.POST)
        user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

        if request.POST:
            co_worker       = request.POST['CoWorkers']
            status          = request.POST['Status']
            no_range_date   = request.POST.get('no_range_date', False)
            filter_date     = datetime.datetime.strptime(request.POST['request_date'], "%d.%m.%Y").date()
            num_object      = request.POST['NumObject']

            if form.is_valid():
                #-------------------- Период дат активен ---------------------------------------
                if num_object == '':
                    if co_worker != '' and status != '' and no_range_date != 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,DateTime_schedule=filter_date,CoWorkers=int(co_worker),Status=int(status))
                    elif co_worker != '' and status != '' and no_range_date == 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,CoWorkers=int(co_worker),Status=int(status))

                    elif co_worker != '' and status == '' and no_range_date != 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,DateTime_schedule=filter_date,CoWorkers=int(co_worker))
                    elif co_worker != '' and status == '' and no_range_date == 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,CoWorkers=int(co_worker))

                    elif co_worker == '' and status != '' and no_range_date != 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,DateTime_schedule=filter_date,Status=int(status))
                    elif co_worker == '' and status != '' and no_range_date == 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,Status=int(status))

                    elif co_worker == '' and status == '' and no_range_date != 'on':
                        args['requests'] = support_request.objects.filter(Company=user_company,DateTime_schedule=filter_date)
                    else:
                        args['requests'] = support_request.objects.filter(Company=user_company)
                else:
                    args['requests'] = support_request.objects.filter(NumObject=num_object)

        args['form'] = request_per_date

        return render_to_response('request_trouble_shooting/request_per_date.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')

def get_new_save_request_item(request, request_id=None):
    global type_request
    args = {}

    if request.user.is_active:
        args.update(csrf(request))

        formset = get_new_save_request(request.POST or None, user=request.user, instance=request_id and support_request.objects.get(id=request_id))

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

            return HttpResponseRedirect('/')

        args['form'] = formset
        args['request_id'] = request_id

        return render_to_response('request_trouble_shooting/request_item.html', args, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return HttpResponseRedirect('/login/')