import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from claim.models import support_request
from claim.forms import get_new_save_request, request_actrequired_fordate
from reference_books.models import ExpandedUserProfile, Status

@login_required
def get_requests_trouble_shooting(request,status='open',page_id=1):
    args = {}
    if page_id == None:
        page_id = 1
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
    status_query = Status.objects.get(slug=status)
    if status=='complete':
        current_page = Paginator(support_request.objects.filter(Company=user_company,Status=status_query.id,DateTime_add__year=datetime.datetime.today().year).order_by('-id'),50)
    else:
        current_page = Paginator(support_request.objects.filter(Company=user_company,Status=status_query.id).order_by('-id'),50)
    args['requests'] = current_page.page(page_id)
    args['status'] = status_query

    return render(request, 'request_list.html', args)


@login_required
def get_requests_actrequired(request):
    args = {}
    args.update(csrf(request))

    form = request_actrequired_fordate(request.POST)
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

    if request.method == 'POST' and form.is_valid():
        args['filter_date'] = filter_date = datetime.datetime.strptime(request.POST['request_date'], "%d.%m.%Y").date()
        args['requests_notgetact'] = support_request.objects.filter(Company=user_company,Required_act=True,Date_act__isnull=True).order_by('-id')
        args['requests_getact'] = support_request.objects.filter(Company=user_company,Required_act=True,Date_act=filter_date).order_by('-id')
    else:
        args['requests_notgetact'] = support_request.objects.filter(Company=user_company,Required_act=True,Date_act__isnull=True).order_by('-id')
    args['form'] = form

    return render(request, 'act_required_list.html', args)


@login_required
def addget_request_trouble_shooting(request, request_id=None):
    args = {}
    args.update(csrf(request))

    form = get_new_save_request(request.POST or None, user=request.user, instance=request_id and support_request.objects.get(id=request_id))

    if request.method == 'POST' and form.is_valid():
        new_request = form.save(commit=False)
        if request_id==None:
            new_request.Create_user = request.user.id
        else:
            new_request.Update_user = request.user.id
        new_request.Company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
        new_request.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('trouble:get_requests',args=['open']))

    else:
        args['form'] = form
        if request_id:
            args['request_data'] = support_request.objects.get(id=request_id)

        return render(request, 'request_item.html', args)