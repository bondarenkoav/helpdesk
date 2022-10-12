# -*- coding: utf-8 -*-
import logging
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from accounts.views import get_scompany, get_cur_scompany
from reference_books.forms import addget_transmitter_form, addget_client_form, addget_coworker_form, addget_routes_form, \
    addget_pcn_form, addget_opsosrate_form, addget_opsosname_form
from reference_books.models import ModelTransmitter, Client, CoWorker, RoutesMaintenance, SystemPCN, OpSoS_rate, \
    OpSoS_name

url_area = 'reference_books'
logger = logging.getLogger(__name__)


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
def get_opsosnames(request):
    paginator = Paginator(OpSoS_name.objects.all(), 15)
    page = request.GET.get('page')
    try:
        opsosname = paginator.page(page)
    except PageNotAnInteger:
        opsosname = paginator.page(1)
    except EmptyPage:
        opsosname = paginator.page(paginator.num_pages)

    return render(request, 'opsosname_list.html', {
        'title': 'Сотовые операторы',
        'list': opsosname,
        'page': page,
        'url_addget': '%s:addget_opsosnames' % url_area
    })

@login_required
@csrf_protect
def addget_opsosname(request, name_id=None):
    form = addget_opsosname_form(request.POST or None, instance=name_id and OpSoS_name.objects.get(id=name_id))
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('reference_books:get_opsosnames')
    else:
        return render(request, 'template_item.html', {
            'title': 'Сотовый оператор',
            'form': form,
            'data': OpSoS_name.objects.filter(id=name_id).last(),
            'url_getlist': '%s:get_opsosnames' % url_area,
            'url_addget': '%s:addget_opsosname' % url_area
        })


@login_required
def get_opsosrates(request):
    paginator = Paginator(OpSoS_rate.objects.all(), 15)
    page = request.GET.get('page')
    try:
        opsosrate = paginator.page(page)
    except PageNotAnInteger:
        opsosrate = paginator.page(1)
    except EmptyPage:
        opsosrate = paginator.page(paginator.num_pages)

    return render(request, 'opsosrate_list.html', {
        'title': 'Тарифы',
        'list': opsosrate,
        'page': page,
        'url_addget': '%s:addget_opsosrate' % url_area
    })


@login_required
@csrf_protect
def addget_opsosrate(request, rate_id=None):
    form = addget_opsosrate_form(request.POST or None, instance=rate_id and OpSoS_rate.objects.get(id=rate_id))

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('reference_books:get_opsosrates')
    else:
        return render(request, 'template_item.html', {
            'title': 'Тариф',
            'form': form,
            'data': OpSoS_rate.objects.filter(id=rate_id).last(),
            'url_getlist': '%s:get_opsosrates' % url_area,
            'url_addget': '%s:addget_opsosrate' % url_area
        })


@login_required
def get_pcn(request):
    paginator = Paginator(SystemPCN.objects.all(), 15)
    page = request.GET.get('page')
    try:
        pcn = paginator.page(page)
    except PageNotAnInteger:
        pcn = paginator.page(1)
    except EmptyPage:
        pcn = paginator.page(paginator.num_pages)

    return render(request, 'pcn_list.html', {
        'title': 'ПЦН',
        'list': pcn,
        'page': page,
        'url_addget': '%s:addget_pcn' % url_area
    })


@login_required
@csrf_protect
def addget_pcn(request, pcn_id=None):
    form = addget_pcn_form(request.POST or None, instance=pcn_id and SystemPCN.objects.get(id=pcn_id))
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('reference_books:get_pcn')
    else:
        return render(request, 'template_item.html', {
            'title': 'ПЦН',
            'form': form,
            'data': SystemPCN.objects.filter(id=pcn_id).last(),
            'url_getlist': '%s:get_pcn' % url_area,
            'url_addget': '%s:addget_pcn' % url_area
        })


@login_required
def get_transmitters(request):
    paginator = Paginator(ModelTransmitter.objects.all(), 15)
    page = request.GET.get('page')
    try:
        transmitters = paginator.page(page)
    except PageNotAnInteger:
        transmitters = paginator.page(1)
    except EmptyPage:
        transmitters = paginator.page(paginator.num_pages)

    return render(request, 'transmitters_list.html', {
        'title': 'Передатчики',
        'list': transmitters,
        'page': page,
        'url_addget': '%s:addget_transmitter' % url_area
    })


@login_required
@csrf_protect
def addget_transmitter(request, transmitter_id=None):
    form = addget_transmitter_form(request.POST or None, instance=transmitter_id and ModelTransmitter.objects.get(id=transmitter_id))
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('reference_books:get_transmitters')
    else:
        return render(request, 'template_item.html', {
            'title': 'Передатчик',
            'form': form,
            'data': SystemPCN.objects.filter(id=transmitter_id).last(),
            'url_getlist': '%s:get_transmitters' % url_area,
            'url_addget': '%s:addget_transmitter' % url_area
        })


@login_required
def get_clients(request):
    paginator = Paginator(Client.objects.filter(ServiceCompany=get_cur_scompany(request.user)), 15)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, 'clients_list.html', {
        'title': 'Контрагенты',
        'list': clients,
        'page': page,
        'url_addget': '%s:addget_client' % url_area
    })

@login_required
@csrf_protect
def addget_client(request, client_id=None):
    form = addget_client_form(request.POST or None, user=request.user, instance=client_id and Client.objects.get(id=client_id))
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('reference_books:get_clients')
    else:
        return render(request, 'template_item.html', {
            'title': 'Контрагент',
            'form': form,
            'data': Client.objects.filter(id=client_id).last(),
            'url_getlist': '%s:get_clients' % url_area,
            'url_addget': '%s:addget_client' % url_area
        })


@login_required
def get_coworkers(request):
    paginator = Paginator(CoWorker.objects.filter(ServiceCompany=get_cur_scompany(request.user)), 15)
    page = request.GET.get('page')
    try:
        coworks = paginator.page(page)
    except PageNotAnInteger:
        coworks = paginator.page(1)
    except EmptyPage:
        coworks = paginator.page(paginator.num_pages)

    return render(request, 'coworker_list.html', {
        'title': 'Исполнители',
        'list': coworks,
        'page': page,
        'url_addget': '%s:addget_coworker' % url_area
    })

@login_required
@csrf_protect
def addget_coworker(request, coworker_id=None):
    form = addget_coworker_form(request.POST or None, user=request.user, instance=coworker_id and CoWorker.objects.get(id=coworker_id))
    if request.POST:
        if form.is_valid():
            form.save()
            form.save_m2m()
            return redirect('reference_books:get_coworkers')
    else:
        return render(request, 'template_item.html', {
            'title': 'Сотрудники',
            'form': form,
            'data': CoWorker.objects.filter(id=coworker_id).last(),
            'url_getlist': '%s:get_coworkers' % url_area,
            'url_addget': '%s:addget_coworker' % url_area
        })


@login_required
def get_routs(request):
    paginator = Paginator(RoutesMaintenance.objects.filter(ServiceCompany=get_cur_scompany(request.user)).
                          order_by('Number'), 10)
    page = request.GET.get('page')
    try:
        routs = paginator.page(page)
    except PageNotAnInteger:
        routs = paginator.page(1)
    except EmptyPage:
        routs = paginator.page(paginator.num_pages)

    return render(request, 'routs_list.html', {
        'title': 'Маршруты',
        'list': routs,
        'page': page,
        'url_addget': '%s:addget_rout' % url_area
    })

@login_required
@csrf_protect
def addget_rout(request, routes_id=None):
    form = addget_routes_form(request.POST or None, user=request.user, instance=routes_id and RoutesMaintenance.objects.get(id=routes_id))
    if request.POST:
        if form.is_valid():
            form.save()
            redirect('reference_books:get_routs')
    else:
        return render(request, 'template_item.html', {
            'title': 'Маршрут ТО',
            'form': form,
            'data': RoutesMaintenance.objects.filter(id=routes_id).last(),
            'url_getlist': '%s:get_coworkers' % url_area,
            'url_addget': '%s:addget_rout' % url_area
        })
