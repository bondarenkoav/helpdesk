import datetime
import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect

from accounts.views import get_cur_scompany
from dashboard.views import logging_event
from exploitation.models import eproposals as exploitation_proposal
from maintenance.apps import MaintenanceAppConfig
from maintenance.models import mobjects, mproposals, mtroubles, mproposals_filter, mobjects_filter, mtroubles_filter
from maintenance.forms import get_add_request_to, get_add_trouble_form, get_add_object_to, get_request_routs
from reference_books.models import Status, TypeRequest, TypeDocument, RoutesMaintenance, Event

logger = logging.getLogger(__name__)

events = Event.objects.all()

app = MaintenanceAppConfig.name


@login_required
@permission_required('maintenance.custom_view_object', login_url=reverse_lazy('page_error403'))
def get_mobjects(request, status='work'):
    objects_list = mobjects.objects.filter(ServiceCompany=get_cur_scompany(request.user))
    if status == 'work':
        objects_list = objects_list.filter(Status_object=True)
    else:
        objects_list = objects_list.filter(Status_object=False)

    qs = objects_list.order_by('id')
    objects_filter = mobjects_filter(request.GET, queryset=qs)
    paginator = Paginator(objects_filter.qs, 20)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    objects_filter = mobjects_filter(request.GET, queryset=qs)

    return render(request, 'mobject_list.html', {
        'title': 'Объекты ТО',
        'status': status,
        'objects': objects,
        'page': page,
        'objects_filter': objects_filter,
    })


@login_required
@permission_required('maintenance.custom_view_object', login_url=reverse_lazy('page_error403'))
@csrf_protect
def addget_mobjects(request, object_id=None):
    object_data = olddata = []
    ts_string = ms_string = ''
    if object_id:
        object_data = mobjects.objects.get(id=object_id)

    form = get_add_object_to(request.POST or None, user=request.user,
                             instance=object_id and mobjects.objects.get(id=object_id))

    if request.POST:
        if form.is_valid():
            new_object = form.save(commit=False)
            if object_id is None:
                new_object.TypeRequest = TypeRequest.objects.get(slug='maintenance')
                new_object.TypeDocument = TypeDocument.objects.get(slug='object')
            else:
                olddata = mobjects.objects.get(id=object_id)
                new_object.Client_choices = olddata.Client_choices
                new_object.ServiceCompany = olddata.ServiceCompany
            new_object.save()
            form.save_m2m()

            if object_id is None:
                try:
                    logging_event(app, 'request', new_object.pk, events.get(slug='Object_add'), old_value='')
                except:
                    logger.error(u'|%s|: Ошибка добавления объетка ТО' % request.user.username)
            else:
                try:
                    if new_object.NumObject != olddata.NumObject:
                        logging_event(app, 'object', new_object.pk, events.get(slug='NumObj_change'),
                                      old_value=olddata.NumObject)
                    if new_object.AddressObject != olddata.AddressObject:
                        logging_event(app, 'object', new_object.pk, events.get(slug='AddressObj_change'),
                                      old_value=olddata.AddressObject)
                    if new_object.TypeSecurity != olddata.TypeSecurity:
                        for ts_item in olddata.TypeSecurity.objects.all():
                            if ts_string == '':
                                ts_string = ts_item.Name
                            else:
                                ts_string = ts_string + ', ' + ts_item.Name
                        logging_event(app, 'object', new_object.pk, events.get(slug='TypeSecurity_change'),
                                      old_value=olddata.ts_string)
                    if new_object.Month_schedule != olddata.Month_schedule:
                        for ms_item in olddata.Month_schedule.objects.all():
                            if ms_string == '':
                                ms_string = ms_item.Month_name
                            else:
                                ms_string = ms_string + ', ' + ms_item.Month_name
                        logging_event(app, 'object', new_object.pk, events.get(slug='Month_schedule_change'),
                                      old_value=olddata.ms_string)
                    if new_object.Routes != olddata.Routes:
                        logging_event(app, 'object', new_object.pk, events.get(slug='Route_change'),
                                      old_value=olddata.Routes.Descript)
                    if new_object.Date_open != olddata.Date_open or new_object.Date_end != olddata.Date_end:
                        period = olddata.Date_open.__str__() + '-' + olddata.Date_end.__str__()
                        logging_event(app, 'object', new_object.pk, events.get(slug='PeriodMaintenance_change'),
                                      old_value=period)
                    if new_object.Status_object != olddata.Status_object:
                        logging_event(app, 'object', new_object.pk, events.get(slug='Status_change'),
                                      old_value=olddata.Status_object.__str__())
                except:
                    logger.error(u'|%s|: Ошибка обновления объекта ТО' % request.user.username)

            return redirect('close_tab')

    return render(request, 'mobject_item.html', {
        'form': form,
        'object_data': object_data
    })


@login_required
@permission_required('maintenance.custom_view', login_url=reverse_lazy('page_error403'))
def get_mproposals(request, status='open'):
    objects = mobjects.objects.filter(ServiceCompany=get_cur_scompany(request.user))
    proposals_list = mproposals.objects.filter(Object__in=objects, Status=Status.objects.get(slug=status)).order_by(
        '-DateTime_add')
    proposals_filter = mproposals_filter(request.GET, queryset=proposals_list)

    paginator = Paginator(proposals_filter.qs, 20)
    page = request.GET.get('page')
    try:
        proposals = paginator.page(page)
    except PageNotAnInteger:
        proposals = paginator.page(1)
    except EmptyPage:
        proposals = paginator.page(paginator.num_pages)

    return render(request, 'mproposals_list.html', {
        'title': 'Заявки ТО',
        'status': status,
        'proposals': proposals,
        'page': page,
        'proposals_filter': proposals_filter, }
                  )


@login_required
@permission_required('maintenance.custom_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def addget_mproposals(request, proposal_id=None, object_id=None):
    proposal_data = olddata = []
    cw_string = ''

    if proposal_id:
        proposal_data = mproposals.objects.get(id=proposal_id)

    form = get_add_request_to(request.POST or None, object_id=object_id, instance=proposal_id and proposal_data)
    create_support_request = request.POST.get('create_support_request', False)

    if request.POST:
        if form.is_valid():
            new_proposal = form.save(commit=False)
            if proposal_id is None:
                new_proposal.Object = mobjects.objects.get(id=object_id)
                new_proposal.TypeRequest = TypeRequest.objects.get(slug='maintenance')
                new_proposal.TypeDocument = TypeDocument.objects.get(slug='request')
            else:
                olddata = mproposals.objects.get(id=proposal_id)
            new_proposal.save()
            form.save_m2m()

            if proposal_id is None:
                try:
                    logging_event(app, 'request', new_proposal.pk, events.get(slug='Request_add'), old_value='')
                except:
                    logger.error(u'|%s|: Ошибка добавления заявки ТО' % request.user.username)
            else:
                try:
                    if new_proposal.DateTime_schedule != olddata.DateTime_schedule:
                        logging_event(app, 'request', new_proposal.pk, events.get(slug='DateSchedule_change'),
                                      old_value=olddata.DateTime_schedule.__str__())
                    if new_proposal.DateTime_work != olddata.DateTime_work:
                        logging_event(app, 'request', new_proposal.pk, events.get(slug='DateWork_change'),
                                      old_value=olddata.DateTime_work.__str__())
                    if new_proposal.Status != olddata.Status:
                        logging_event(app, 'request', new_proposal.pk, events.get(slug='Status_change'),
                                      old_value=olddata.Status.Name)
                    if new_proposal.CoWorkers != olddata.CoWorkers:
                        for cw_item in olddata.CoWorkers.objects.all():
                            if cw_string == '':
                                cw_string = cw_item
                            else:
                                cw_string = cw_string + ', ' + cw_item
                        logging_event(app, 'request', new_proposal.pk, events.get(slug='CoWorkers_change'),
                                      old_value=olddata.cw_string)
                except:
                    logger.error(u'|%s|: Ошибка обновления заявки ТО' % request.user.username)

            if create_support_request == 'on':
                proposal_data = mproposals.objects.get(id=proposal_id)
                eproposal = exploitation_proposal.objects.create(
                    NumObject=proposal_data.Object.NumObject,
                    AddressObject=proposal_data.Object.AddressObject,
                    Client=proposal_data.Object.Client.Name,
                    Company=proposal_data.Object.ServiceCompany,
                    Create_user=request.user.id,
                    FaultAppearance=proposal_data.DescriptionWorks,
                    DateTime_schedule=proposal_data.DateTime_work + datetime.timedelta(days=1)
                )
                logger.debug(u'|%s|: Заявка №%d на устранение неисправности в ходе ТО успешно добавлена' % (
                request.user.username, eproposal.id))
            return redirect('close_tab')

    return render(request, 'mproposals_item.html', {
        'form': form,
        'object_data': mobjects.objects.get(id=object_id),
        'proposal_data': proposal_data,
    })


@login_required
@csrf_protect
def get_mproposals_on_routs(request):
    proposals = troubles = []
    form = get_request_routs(request.POST or None, user=request.user)

    if request.POST:
        ch_month = int(request.POST['month_list'])
        ch_year = int(request.POST['year_list'])
        ch_route = int(request.POST['routs'])

        if form.is_valid():
            list_objects = mobjects.objects.filter(ServiceCompany=get_cur_scompany(request.user),
                                                   Routes=RoutesMaintenance.objects.get(id=ch_route))
            proposals = mproposals.objects.filter(Object__in=list_objects,
                                                  DateTime_schedule__month=ch_month,
                                                  DateTime_schedule__year=ch_year,
                                                  Status__in=Status.objects.exclude(slug='canceled'))
            troubles = mtroubles.objects.filter(Status=Status.objects.get(slug='open'),
                                                Routes=RoutesMaintenance.objects.get(id=ch_route))

    return render(request, 'mproposals_routs_list.html', {
        'form': form,
        'proposals': proposals,
        'troubles': troubles,
    })


@login_required
@permission_required('maintenance.custom_view_trouble', login_url=reverse_lazy('page_error403'))
def get_mtroubles(request):
    mtroubles_list = mtroubles.objects.\
        filter(ServiceCompany=get_cur_scompany(request.user)).order_by('Status', 'DateTime_add')
    troubles_filter = mtroubles_filter(request.GET, queryset=mtroubles_list)
    paginator = Paginator(troubles_filter.qs, 20)
    page = request.GET.get('page')
    try:
        troubles = paginator.page(page)
    except PageNotAnInteger:
        troubles = paginator.page(1)
    except EmptyPage:
        troubles = paginator.page(paginator.num_pages)

    return render(request, 'mtrouble_list.html', {
        'title': 'Заявки на устранение неисправностей во время ТО',
        'troubles': troubles,
        'page': page,
        'mtroubles_filter': troubles_filter
    })


@login_required
@permission_required('maintenance.custom_view_trouble', login_url=reverse_lazy('page_error403'))
@csrf_protect
def addget_mtroubles(request, trouble_id=None):
    if trouble_id:
        trouble_data = mtroubles.objects.get(id=trouble_id)
    else:
        trouble_data = None

    form = get_add_trouble_form(request.POST or None, user=request.user,
                                instance=trouble_id and mtroubles.objects.get(id=trouble_id))

    if request.POST:
        if form.is_valid():
            new_trouble = form.save(commit=False)
            if trouble_id is None:
                new_trouble.ServiceCompany = get_cur_scompany(request.user)
                new_trouble.Create_user = request.user
                new_trouble.TypeRequest = TypeRequest.objects.get(slug='maintenance')
                new_trouble.TypeDocument = TypeDocument.objects.get(slug='trouble')
            else:
                olddata = mtroubles.objects.get(id=trouble_id)
                new_trouble.ServiceCompany = olddata.ServiceCompany
                new_trouble.AddressObject = olddata.AddressObject
                new_trouble.FaultAppearance = olddata.FaultAppearance
                new_trouble.Update_user = request.user
            new_trouble.save()
            form.save_m2m()

            if trouble_id is None:
                logger.debug(u'|%s|: Заявка добавлена' % request.user.username)
            else:
                logger.debug(u'|%s|: Заявка №%d обновлена' % (request.user.username, new_trouble.pk))

            return redirect('close_tab')
        else:
            return render(request, 'mtrouble_item.html', {'form': form})
    else:
        return render(request, 'mtrouble_item.html', {
            'form': form,
            'trouble_data': trouble_data
        })