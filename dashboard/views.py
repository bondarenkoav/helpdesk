import datetime
import re

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

from accounts.models import Profile
from accounts.views import get_cur_scompany
from build.models import bacts as build_acts, bproposals
from dashboard.forms import search_form, events_form
from dashboard.models import logging
from exploitation.models import eproposals
from maintenance.models import mproposals, mobjects, count_completeproposals_per_month
from reference_books.models import Status, CoWorker, Client, Month_list, Event, TypeRequest, ServiceCompanies

__author__ = 'ipman'


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def index(request):
    if bool(request.user.groups.filter(name='engineers')):
        return redirect('exploitation:get_eproposals_engineer')
    if request.user.groups.count() == 0:
        return redirect('page_error423')
    profile = Profile.objects.get(user=request.user)

    if profile.birthday is None or profile.phone is None:
        return redirect('update_profile')

    charts_data = count_completeproposals_per_month.objects.all(),
    list_years = count_completeproposals_per_month.objects.filter(
        dyear__range=(datetime.datetime.today().year-2, datetime.datetime.today().year)).distinct('dyear')

    return render(request, 'dashboard.html', {
        'user': request.user,
        'charts_data': charts_data,
        'list_years': list_years,
        'list_month': Month_list.objects.all(),
    })


# Получаем список активных пользователей
def get_activeusers():
    # 15 минут - время на активные действия в программе
    session_start = datetime.datetime.now() - datetime.timedelta(minutes=15)
    uid_list = []
    try:
        sessions = Session.objects.filter(expire_date__gte=session_start)
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
    except:
        pass
    return User.objects.filter(id__in=uid_list)


@login_required
@csrf_protect
def search_requests(request):
    form = search_form(request.POST or None, user=request.user)
    result = []

    if request.POST:
        if form.is_valid():
            typedates = request.POST.get('typedates', None)
            startdate = datetime.datetime.strptime(request.POST['startdate'], '%Y-%m-%d')

            if request.POST['enddate']:
                enddate = datetime.datetime.strptime(request.POST['enddate'], '%Y-%m-%d')
            else:
                enddate = startdate

            norangedate = request.POST.get('norangedate', False)
            typerequest = request.POST.get('typerequest', None)
            set = request.POST.get('set', False)
            status = request.POST.get('status', None)
            coworker = request.POST.get('coworkers', None)
            numobject = request.POST['numobject']
            adrobject = request.POST['adrobject']
            client = request.POST.get('clients', None)

            cur_scompany = get_cur_scompany(request.user)

            if status:
                soargs = (Q(Status__in=Status.objects.filter(id=int(status))))
            else:
                soargs = (Q(Status__in=Status.objects.all()))

            if client:
                clargs = (Q(Client_choices__in=Client.objects.filter(Name__icontains=client)) | Q(
                    Client_words__icontains=client))
            else:
                clargs = (Q(Client_choices__in=Client.objects.all()) | Q(Client_choices=None))

            if coworker:
                cwargs = (Q(CoWorkers__in=CoWorker.objects.filter(id=int(coworker))))
            else:
                cwargs = (Q(CoWorkers__in=CoWorker.objects.filter(ServiceCompany=cur_scompany)) | Q(CoWorkers=None))

            if typedates == 'schedule':
                dtargs = (Q(DateTime_schedule__range=(startdate, enddate)))
            else:
                dtargs = (Q(DateTime_work__range=(startdate, enddate)))

            result = exploit_s = build_s = mprop_s = mobject_s = eproposals.objects.none()
            message1 = message2 = ''

            if typerequest == 'exploitation':
                exploit_s = eproposals.objects.filter(ServiceCompany=cur_scompany)
            elif typerequest == 'build':
                build_s = bproposals.objects.filter(ServiceCompany=cur_scompany)
            else:
                mobject_s = mobjects.objects.filter(clargs, ServiceCompany=cur_scompany)
                mprop_s = mproposals.objects.filter(Object__in=mobject_s)

            # -------------------- Период дат активен ---------------------------------------
            if adrobject:
                # ------------- Подготовка адреса -------------------------
                adrobject_rev = ''
                for i in list(reversed(re.split(r'\s', adrobject))):
                    if adrobject_rev != '':
                        adrobject_rev = adrobject_rev + ' ' + i
                    else:
                        adrobject_rev = i
                search_regex_asc = r"%s" % re.sub(r'\s', '.+', adrobject)
                search_regex_desc = r"%s" % re.sub(r'\s', '.+', adrobject_rev)
                adargs = (Q(AddressObject__iregex=search_regex_asc) | Q(AddressObject__iregex=search_regex_desc))
                # ---------------------------------------------------------
                if typerequest == 'exploitation':
                    result = exploit_s.filter(adargs)
                elif typerequest == 'build':
                    result = build_s.filter(adargs)
                else:
                    mobject_s = mobjects.objects.filter(adargs, ServiceCompany=cur_scompany)
                    result = mproposals.objects.filter(Object__in=mobject_s)

            elif numobject:
                # ------------- Подготовка номера -------------------------
                numobject = re.sub(r'\s', '', numobject)
                noargs = (Q(NumObject__icontains=numobject))
                # ---------------------------------------------------------
                if typerequest == 'exploitation':
                    result = exploit_s.filter(noargs)
                elif typerequest == 'maintenance':
                    result = mproposals.objects.filter(Object__in=mobjects.filter(noargs))

            elif norangedate:
                if typerequest == 'exploitation':
                    result = exploit_s.filter(cwargs, soargs, clargs)
                elif typerequest == 'build':
                    acts = build_acts.objects.filter(cwargs).values('proposal').distinct()
                    result = build_s.filter(soargs, clargs, id__in=acts)
                else:
                    result = mprop_s.filter(cwargs, soargs)

            else:
                if typerequest == 'exploitation':
                    result = exploit_s.filter(cwargs, soargs, clargs, dtargs)
                elif typerequest == 'build':
                    acts = build_acts.objects.filter(cwargs).values('proposal').distinct()
                    result = build_s.filter(dtargs, soargs, clargs, id__in=acts)
                else:  # typerequest == 'maintenance'
                    result = mprop_s.filter(cwargs, soargs, dtargs)

            result = result.distinct('id').order_by('-id')

            if set == 'requests':
                mobject_s = None
            elif set == 'objects':
                result = None

            if result is None:
                messages.info(request, 'Нет результатов поиска. Попробуйте изменить параметры поиска!')

            return render(request, 'search.html',
                          {'form': form, 'requests': result, 'objects': mobject_s, 'type': typerequest,
                           'message_result': message1, 'message_object': message2})

    return render(request, 'search.html', {'form': form})


@login_required
@csrf_protect
def journal_events(request):
    events = []
    scompany_data = None

    form = events_form(request.POST or None)
    if request.POST:
        if form.is_valid():
            app_data = form.cleaned_data.get('filter_app')
            start_date = form.cleaned_data['filter_start_date']
            end_date = form.cleaned_data['filter_end_date']
            event = form.cleaned_data.get('filter_typeevent')
            scompany = form.cleaned_data.get('filter_scompany')

            events = logging.objects.filter(add_date__date__range=(start_date, end_date), app__in=app_data, scompany=scompany)
            if event:
                events = events.filter(event_code=event)

    return render(request, 'events.html', {
        'form': form,
        'title': u'Произведенные операции',
        'title_small': u'Журналы',
        'scompany': scompany_data,
        'list': events
    })


def logging_event(app, dct_type, dct_id, event, old_value=''):
    logging.objects.create(app=TypeRequest.objects.get(slug=app), type_dct=dct_type, dct_id=dct_id,
                           event=Event.objects.get(slug=event), old_value=old_value)


def close_tab(request):
    return render(request, 'close_tab.html')
