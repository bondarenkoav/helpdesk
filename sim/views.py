import logging

import openpyxl
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from accounts.views import get_cur_scompany, clean_phone
from sim.forms import get_new_simcard
from sim.models import OpSoS_card, OpSoS_card_filter


logger = logging.getLogger(__name__)


def clean_iccsim(icc_sim):
    return icc_sim.replace(' ', '')


@login_required
def get_simcard_list(request):
    qs = OpSoS_card.objects.filter(ServiceCompany=get_cur_scompany(request.user), archive=False).order_by('id')
    sim_filter = OpSoS_card_filter(request.GET, queryset=qs)
    paginator = Paginator(sim_filter.qs, 20)
    page = request.GET.get('page')
    try:
        sim = paginator.page(page)
    except PageNotAnInteger:
        sim = paginator.page(1)
    except EmptyPage:
        sim = paginator.page(paginator.num_pages)
    sim_filter = OpSoS_card_filter(request.GET, queryset=qs)

    return render(request, 'simcard_list.html', {
        'title': 'Активные SIM-карты',
        'opsoscard': sim,
        'page': page,
        'opsoscard_filter': sim_filter,
    })


@login_required
def get_simcard_archive_list(request):
    qs = OpSoS_card.objects.filter(ServiceCompany=get_cur_scompany(request.user), archive=True).order_by('id')
    sim_filter = OpSoS_card_filter(request.GET, queryset=qs)
    paginator = Paginator(sim_filter.qs, 20)
    page = request.GET.get('page')
    try:
        sim = paginator.page(page)
    except PageNotAnInteger:
        sim = paginator.page(1)
    except EmptyPage:
        sim = paginator.page(paginator.num_pages)
    sim_filter = OpSoS_card_filter(request.GET, queryset=qs)

    return render(request, 'simcard_list.html', {
        'title': 'Архив SIM-карт',
        'opsoscard': sim,
        'page': page,
        'opsoscard_filter': sim_filter,
    })


@login_required
@csrf_protect
def get_new_simcard_item(request, simcard_id=None):
    if simcard_id:
        simcard_data = OpSoS_card.objects.get(id=simcard_id)
    else:
        simcard_data = OpSoS_card.objects.none()

    form = get_new_simcard(request.POST or None, user=request.user, instance=simcard_id and OpSoS_card.objects.get(id=simcard_id))

    if request.POST:
        if form.is_valid():
            new_sim = form.save(commit=False)
            if simcard_id:
                old_data = OpSoS_card.objects.get(id=simcard_id)
                new_sim.Number_SIM = old_data.Number_SIM
                new_sim.ServiceCompany = old_data.ServiceCompany
                if form.cleaned_data['archive'] is True:
                    new_sim.Status = False
            else:
                new_sim.Number_SIM = clean_phone(form.cleaned_data['Number_SIM'])
                new_sim.ServiceCompany = get_cur_scompany(request.user)
            new_sim.save()

            if simcard_id:
                logger.debug(u'|%s|: СИМ добавлена' % request.user.username)
            else:
                logger.debug(u'|%s|: СИМ №%d обновлена' % (request.user.username, new_sim.pk))

            return redirect('close_tab')

    return render(request, 'simcard_item.html', {
        'form': form,
        'simcard_data': simcard_data
    })


@login_required
@csrf_protect
def parseExcel(request):
    excel_data = ()

    # form = get_ExcelFile()
    if request.POST:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

    return render(request, 'import_sim.html', {
        "excel_data": excel_data,
    })
