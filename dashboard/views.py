from datetime import datetime
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from build.models import build_request
from claim.models import support_request
from dashboard.forms import LoginForm, search_form
from maintenance.models import maintenance_request
from reference_books.models import ExpandedUserProfile


# def log_in(request):
#     args = {}
#     args.update(csrf(request))
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             if form.get_user():
#                 login(request, form.get_user())
#                 return HttpResponseRedirect(reverse(':get_requests'))
#     else:
#         args['form'] = LoginForm()
#     return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


def get_user_perms(request):
    user = get_object_or_404(User, pk=request.user.id)
    return {
        'add'    : user.has_perm('claim.add_bar'),
        'change' : user.has_perm('claim.change_bar'),
        'delete' : user.has_perm('claim.delete_bar'),
    }


# def custom_proc(request):
#     return {
#         'nodes'             : CategoryMenu.objects.all(),
#         'app'               : 'АРМ "Заявки"',
#         'owner'             : 'Группа предприятий "Амулет"',
#         'user'              : request.user,
#         'developer_name'    : 'Бондаренко А.В.',
#         'developer_email'   : 'printex.orsk@gmail.com',
#         'user_group'        : request.user.groups.values('name'),
#     }


@login_required
def index(request):
    return render(request, 'dashboard.html')


@login_required
def search_requests(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = search_form(request.POST) #, user=request.user)

        if form.is_valid():
            coworker        = request.POST['coworkers']
            status          = request.POST['status']
            typerequest     = request.POST['typerequest']
            norangedate     = request.POST.get('norangedate', False)
            requestdate     = datetime.strptime(request.POST['requestdate'], "%d.%m.%Y").date()
            numobject       = request.POST['numobject']
            user_company    = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

            #-------------------- Период дат активен ---------------------------------------
            if typerequest == 'trouble':
                if numobject == '':
                    if coworker != '' and status != '' and norangedate != 'on':
                        req = support_request.objects.filter(Company=user_company,DateTime_schedule=requestdate,CoWorkers=int(coworker),Status=int(status))
                    elif coworker != '' and status != '' and norangedate == 'on':
                        req = support_request.objects.filter(Company=user_company,CoWorkers=int(coworker),Status=int(status))
                    elif coworker != '' and status == '' and norangedate != 'on':
                        req = support_request.objects.filter(Company=user_company,DateTime_schedule=requestdate,CoWorkers=int(coworker))
                    elif coworker != '' and status == '' and norangedate == 'on':
                        req = support_request.objects.filter(Company=user_company,CoWorkers=int(coworker))
                    elif coworker == '' and status != '' and norangedate != 'on':
                        req = support_request.objects.filter(Company=user_company,DateTime_schedule=requestdate,Status=int(status))
                    elif coworker == '' and status != '' and norangedate == 'on':
                        req = support_request.objects.filter(Company=user_company,Status=int(status))
                    elif coworker == '' and status == '' and norangedate != 'on':
                        req = support_request.objects.filter(Company=user_company,DateTime_schedule=requestdate)
                    else:
                        req = support_request.objects.filter(Company=user_company)
                else:
                    req = support_request.objects.filter(NumObject=numobject)

            elif typerequest == 'build':
                if status != '' and norangedate != 'on':
                    req = build_request.objects.filter(Company=user_company,DateTime_schedule=requestdate,Status=int(status))
                elif status != '' and norangedate == 'on':
                    req = build_request.objects.filter(Company=user_company,Status=int(status))
                elif status == '' and norangedate != 'on':
                    req = build_request.objects.filter(Company=user_company,DateTime_schedule=requestdate)
                else:
                    req = build_request.objects.filter(Company=user_company)

            else:
                if numobject == '':
                    if coworker != '' and status != '' and norangedate != 'on':
                        req = maintenance_request.objects.filter(DateTime_schedule=requestdate,CoWorkers=int(coworker),Status=int(status))
                    elif coworker != '' and status != '' and norangedate == 'on':
                        req = maintenance_request.objects.filter(CoWorkers=int(coworker),Status=int(status))
                    elif coworker != '' and status == '' and norangedate != 'on':
                        req = maintenance_request.objects.filter(DateTime_schedule=requestdate,CoWorkers=int(coworker))
                    elif coworker != '' and status == '' and norangedate == 'on':
                        req = maintenance_request.objects.filter(CoWorkers=int(coworker))
                    elif coworker == '' and status != '' and norangedate != 'on':
                        req = maintenance_request.objects.filter(DateTime_schedule=requestdate,Status=int(status))
                    elif coworker == '' and status != '' and norangedate == 'on':
                        req = maintenance_request.objects.filter(Status=int(status))
                    else:
                        req = maintenance_request.objects.filter(DateTime_schedule=requestdate)
                else:
                    req = maintenance_request.objects.filter(NumObject=numobject)

            args['requests'] = req
            args['type'] = typerequest
            args['form'] = search_form(data={'requestdate':requestdate,
                                             'norangedate':norangedate,
                                             'typerequest':typerequest,
                                             'coworkers':coworker,
                                             'status':status,
                                             'numobject':numobject})
            return render(request, 'search.html', args)
        else:
            return render(request, 'search.html', {'form': form})
    else:
        args['form'] = search_form
    return render(request, 'search.html', args)