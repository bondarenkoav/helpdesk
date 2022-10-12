import logging
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect

from accounts.views import get_cur_scompany
from build.apps import BuildAppConfig
from build.forms import get_new_save_acts_build, get_new_save_request
from build.models import bacts, bproposals, bproposals_filter
from dashboard.views import logging_event
from reference_books.models import Status, TypeRequest, TypeDocument, Event, TypeBuild
from tasks.models import user_task

logger = logging.getLogger(__name__)

events = Event.objects.all()

app = BuildAppConfig.name

@login_required
@permission_required('build.custom_view', login_url=reverse_lazy('page_error403'))
def get_bproposals(request, status='open'):
    qs = bproposals.objects.filter(
        ServiceCompany=get_cur_scompany(request.user),
        Status=Status.objects.get(slug=status)).order_by('-id')
    proposals_filter = bproposals_filter(request.GET, queryset=qs)
    paginator = Paginator(proposals_filter.qs, 20)
    page = request.GET.get('page')
    try:
        proposals = paginator.page(page)
    except PageNotAnInteger:
        proposals = paginator.page(1)
    except EmptyPage:
        proposals = paginator.page(paginator.num_pages)
    proposals_filter = bproposals_filter(request.GET, queryset=qs)

    return render(request, 'bproposals_list.html', {
        'title': 'Заявки на эксплуатацию',
        'status': status,
        'proposals': proposals,
        'page': page,
        'proposals_filter': proposals_filter
    })


@login_required
@permission_required('build.custom_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def addget_bproposals(request, proposal_id=None):
    proposal_data = acts = olddata = []
    tb_string = ''
    if proposal_id:
        proposal_data = bproposals.objects.get(id=proposal_id)
        acts = bacts.objects.filter(proposal=proposal_id)

    form = get_new_save_request(request.POST or None, user=request.user, instance=proposal_id and proposal_data)

    if request.POST:
        if form.is_valid():
            new_request = form.save(commit=False)
            if proposal_id is None:
                new_request.TypeRequest = TypeRequest.objects.get(slug='build')
                new_request.TypeDocument = TypeDocument.objects.get(slug='request')
            else:
                olddata = bproposals.objects.get(id=proposal_id)
                new_request.ServiceCompany = olddata.ServiceCompany
                new_request.TypeRequest = olddata.TypeRequest
                new_request.TypeBuild = olddata.TypeBuild
            new_request.save()
            form.save_m2m()

            if proposal_id is None:
                try:
                    logging_event(app, 'request', new_request.pk, events.get(slug='Request_add'), old_value='')
                except:
                    logger.error(u'|%s|: Ошибка добавления заявки на монтаж' % request.user.username)
            else:
                try:
                    if new_request.TypeBuild != olddata.TypeBuild:
                        for tb_item in olddata.TypeBuild.objects.all():
                            if tb_string == '':
                                tb_string = tb_item
                            else:
                                tb_string = tb_string + ', ' + tb_item
                        logging_event(app, 'request', new_request.pk, events.get(slug='TypeSecurity_change'),
                                      old_value=tb_string)
                    if new_request.Client_choices != olddata.Client_choices:
                        logging_event(app, 'request', new_request.pk, events.get(slug='Client_change'),
                                      old_value=olddata.Client_choices.Name)
                    if new_request.AddressObject != olddata.AddressObject:
                        logging_event(app, 'request', new_request.pk, events.get(slug='AddressObj_change'),
                                      old_value=olddata.AddressObject)
                    if new_request.DateTime_schedule != olddata.DateTime_schedule:
                        logging_event(app, 'request', new_request.pk, events.get(slug='DateSchedule_change'),
                                      old_value=olddata.DateTime_schedule.__str__())
                    if new_request.DateTime_work != olddata.DateTime_work:
                        logging_event(app, 'request', new_request.pk, events.get(slug='DateWork_change'),
                                      old_value=olddata.DateTime_work.__str__())
                    if new_request.Status != olddata.Status:
                        logging_event(app, 'request', new_request.pk, events.get(slug='Status_change'),
                                      old_value=olddata.Status.Name)
                except:
                    logger.error(u'|%s|: Ошибка обновления заявки на монтаж' % request.user.username)

            return redirect('close_tab')

    return render(request, 'bproposals_item.html', {
        'form': form,
        'proposal_data': proposal_data,
        'acts': acts
    })


@login_required
def get_bacts(request, page_id=1):
    list_acts = bacts.objects.all()
    current_page = Paginator(list_acts,20)
    return render(request, 'act_list.html', {'acts': current_page.page(page_id)})


@login_required
@csrf_protect
def addget_bacts(request, proposal_id=None, act_id=None):
    act_data = []
    if act_id:
        act_data = bacts.objects.get(id=act_id)

    form = get_new_save_acts_build(request.POST or None, proposal_id=proposal_id, instance=act_id and bacts.objects.get(id=act_id))

    if request.POST:
        if form.is_valid():
            new_act = form.save(commit=False)
            new_act.proposal = bproposals.objects.get(id=proposal_id)
            new_act.save()
            form.save_m2m()

            if act_id is None:
                try:
                    logging_event(app, 'act', new_act.pk, events.get(slug='Act_add'), old_value='')
                except:
                    logger.error(u'|%s|: Ошибка добавления заявки на монтаж' % request.user.username)

            return redirect('build:addget_bproposals', proposal_id=proposal_id)

    return render(request, 'act_item.html', {
        'form': form,
        'act_data': act_data,
        'proposal_data': bproposals.objects.get(id=proposal_id)
    })
