# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.urls import reverse
from reference_books.forms import get_new_save_transmitter, get_new_save_client, co_worker_form, get_add_routes
from reference_books.models import ExpandedUserProfile, ModelTransmitter, Client, CoWorker, RoutesMaintenance


def user_company(request):
    return ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany

def client_names(name):
    name = name.replace('"', '')
    name = name.strip(' ')

    OKOPF = ['ООО','ЗАО','АО','ПАО','ИП']
    name_massiv = name.split(' ')

    for item in OKOPF:
        if name_massiv[0] == item:
            name = name.replace(item,'') + ' ' + item.__str__()

    name = name.strip(' ')
    return name

@login_required
def get_transmitters(request):
    return render(request, 'transmitters/transmitters_list.html', {'list_transmitters' : ModelTransmitter.objects.all()})


def get_add_transmitter(request, transmitter_id=None):
    args = {}
    args.update(csrf(request))
    form = get_new_save_transmitter(request.POST or None, instance=transmitter_id and ModelTransmitter.objects.get(id=transmitter_id))

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reference_books:get_transmitters'))

        args['form'] = form
        args['transmitter_id'] = transmitter_id

        return render(request, 'transmitters/transmitters_item.html', args)


def get_clients(request, page_id=1):
    current_page = Paginator(Client.objects.all().order_by('Name'),20)
    return render(request, 'client/clients_list.html', {'list_clients': current_page.page(page_id)})


def get_add_client(request, client_id=None):
    args = {}
    args.update(csrf(request))
    form = get_new_save_client(request.POST or None, instance=client_id and Client.objects.get(id=client_id))

    if request.user.is_active:
        if request.method == 'POST' and form.is_valid():
            name = client_names(request.POST['Name'])
            item = form.save(commit=False)
            item.Name = name
            item.save()
            return HttpResponseRedirect(reverse('reference_books:get_clients'))

        args['form'] = form
        args['client_id'] = client_id

        return render(request, 'client/clients_item.html', args)


def get_coworkers(request, page_id=1):
    args = {}
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
    current_page = Paginator(CoWorker.objects.filter(ServingCompany=user_company).order_by('Person_FIO'),20)
    args['co_worker'] = current_page.page(page_id)
    return render(request, 'coworker/coworker_list.html', args)


def get_add_coworker(request, coworker_id=None):
    args = {}
    args.update(csrf(request))
    form = co_worker_form(request.POST or None, instance=coworker_id and CoWorker.objects.get(id=coworker_id))

    if request.method == 'POST':
        if form.is_valid():
            item = form.save(commit=False)
            item.ServingCompany = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
            item.save()
            return HttpResponseRedirect(reverse('reference_books:get_coworkers'))

    args['form'] = form
    args['coworker_id'] = coworker_id

    return render(request, 'coworker/coworker_item.html', args)


list_months = [[1,u'Январь'],[2,u'Февраль'],[3,u'Март'],
               [4,u'Апрель'],[5,'Май'],[6,u'Июнь'],
               [7,u'Июль'],[8,'Август'],[9,u'Сентябрь'],
               [10,u'Октябрь'],[11,u'Ноябрь'],[12,u'Декабрь']]


def get_routs(request):
    args = {}
    user_company = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
    args['routs'] = RoutesMaintenance.objects.filter(ServingCompany=user_company).order_by('Number')
    return render(request, 'routes/routs_list.html', args)


def get_add_rout(request, routes_id=None):
    args = {}
    args.update(csrf(request))
    form = get_add_routes(request.POST or None, instance=routes_id and RoutesMaintenance.objects.get(id=routes_id))

    if request.method == 'POST':
        if form.is_valid():
            item = form.save(commit=False)
            item.ServingCompany = ExpandedUserProfile.objects.get(UserName=request.user.id).ServingCompany
            item.save()
            return HttpResponseRedirect(reverse('reference_books:get_routs'))

    args['form'] = form
    args['routes_id'] = routes_id
    args['months'] = list_months

    return render(request, 'routes/routs_item.html', args)