import os
import logging
import magic
import requests

from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, FloatField, Sum
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect

from accounts.models import Profile
from dashboard.templatetags.personal_tags import view_shortfio_user
from helpdesk import settings
from helpdesk.settings import EMAIL_HOST_USER
from reference_books.models import Status_task, TypeNotification_task, MaterialsWorks, Status_calc
from tasks.forms import form_add_task, form_calc_operator, form_calc_disposer, form_calc_executor, MaterialsFormSet, \
    form_calc_additional_fields, form_fill_materials
from tasks.models import user_task, tasks_filter, Calculations, CalcHistory, CalcMaterialsWorks, TemplateDocuments, \
    CalcNotify
from accounts.smsc_api import SMSC

__author__ = 'ipman'

content_area = u'Рабочий стол'
logger = logging.getLogger(__name__)


@login_required()
@permission_required('tasks.calc_list_view', login_url=reverse_lazy('page_error403'))
def getlist_calc(request):
    calc_list = Calculations.objects.filter(executor__isnull=False)

    paginator = Paginator(calc_list, 20)
    page = request.GET.get('page')

    try:
        calc = paginator.page(page)
    except PageNotAnInteger:
        calc = paginator.page(1)
    except EmptyPage:
        calc = paginator.page(paginator.num_pages)
    return render(request, 'calc_list.html', {
        'title': u'Список запросов',
        'title_small': u'Запросы',
        'list': calc,
        'page': page,
    })


def add_history(calc_data, event, user, value=None):
    CalcHistory.objects.create(calculation=calc_data, event=event, value=value, user=user)


@login_required
@permission_required('tasks.calc_item_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def calc_operator(request):
    form = form_calc_operator(request.POST or None)

    if request.POST:
        if form.is_valid():
            new_calc = form.save(commit=False)
            new_calc.operator = Profile.objects.get(user=request.user)
            new_calc.Status = Status_calc.objects.get(slug='open')
            new_calc.save()
            form.save_m2m()

            CalcNotify.objects.create(
                calculation=new_calc,
                title="Новый запрос на калькуляцию №%s" % str(new_calc.id),
                group_executor=Group.objects.get(name='disposer'))
            add_history(new_calc, 'Новая заявка на калькуляцию №%d' % new_calc.id, request.user)

            return redirect('dashboard:index')

    return render(request, 'calc_operator.html', {
        'title': 'Ввод запроса на калькуляцию',
        'title_small': 'Работа с клиентом',
        'form': form,
    })


@login_required
@permission_required('tasks.calc_item_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def calc_disposer(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    form = form_calc_disposer(request.POST or None)

    if request.POST:
        if form.is_valid():
            executor = form.cleaned_data.get('executor')
            Calculations.objects.filter(id=calc_id).update(executor=executor,
                                                           disposer=Profile.objects.get(user=request.user),
                                                           Status=Status_calc.objects.get(slug='executor'))

            CalcNotify.objects.create(
                calculation=calc_data, title="Составить калькуляцию №%s" % str(calc_data.id), executor=executor)
            add_history(calc_data, 'Для заявки на калькуляцию №%d выбран исполнитель %s' % (calc_data.id, executor),
                        request.user)

            return redirect('dashboard:index')

    return render(request, 'calc_disposer.html', {
        'title': 'Определение исполнителя',
        'title_small': 'Работа с клиентом',
        'form': form,
        'calc_data': calc_data,
    })


@login_required
@permission_required('tasks.calc_item_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def calc_executor(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    form = form_calc_executor(request.POST or None, request.FILES or None, profile=Profile.objects.get(user=request.user),
                              instance=calc_id and Calculations.objects.get(id=calc_id))

    if request.POST:
        if form.is_valid():
            new_calc = form.save(commit=False)

            if form.cleaned_data['Date_inspection']:
                dt = datetime.combine(form.cleaned_data['Date_inspection'], form.cleaned_data['Time_inspection'])
                if calc_data.DateTime_inspection_object is None:
                    new_calc.Status = Status_calc.objects.get(slug='inspection')
                    add_history(calc_data, 'Установлена дата/время осмотра объекта %s' % dt, request.user)
                new_calc.DateTime_inspection_object = dt
            if form.cleaned_data['Channels_connection'] and calc_data.Channels_connection is None:
                add_history(calc_data, 'Указан канал передачи данных', request.user)

            if form.cleaned_data['client_consent'] is True and calc_data.client_consent is False:
                new_calc.Status = Status_calc.objects.get(slug='reconciliation')
                CalcNotify.objects.create(
                    calculation=calc_data,
                    title="Ознакомтесь с новой калькуляцией №%s" % str(calc_data.id),
                    group_executor=Group.objects.get(name='storekeepers'))
                CalcNotify.objects.create(
                    calculation=calc_data,
                    title="Ознакомтесь с новой калькуляцией №%s" % str(calc_data.id),
                    group_executor=Group.objects.get(name='managers'))

            if form.cleaned_data['Estimate'] and calc_data.Estimate is None:
                new_calc.Status = Status_calc.objects.get(slug='complete')
                add_history(calc_data, 'Загружен скан калькуляции', request.user)
                CalcNotify.objects.create(
                    calculation=calc_data,
                    title="Ознакомтесь с новой калькуляцией №%s" % str(calc_data.id),
                    group_executor=Group.objects.get(name='accountants'))

            new_calc.save()
            form.save_m2m()

    return render(request, 'calc_executor.html', {
        'title': 'Исполнитель',
        'title_small': 'Работа с клиентом',
        'form': form,
        'calc_data': calc_data,
        'history': CalcHistory.objects.filter(calculation=calc_data).order_by('DateTime_add'),
        'materials': CalcMaterialsWorks.objects.filter(calculation=calc_data).order_by('material')
    })


@login_required
@permission_required('tasks.calc_item_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def calc_other(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    
    return render(request, 'calc_other.html', {
        'title': 'Соисполнители',
        'title_small': 'Работа с клиентом',
        'calc_data': calc_data,
        'materials': CalcMaterialsWorks.objects.filter(calculation=calc_data)
    })


def task_notification_author(task_id):
    smsc = SMSC()
    task = user_task.objects.get(id=task_id)

    try:
        profile = Profile.objects.get(user=task.author)
        type_notify = TypeNotification_task.objects.all()

        if task.notification == type_notify.get(slug='sms'):
            text = "АРМ 'Заявки'. Поставленая задача %s сменила статус на %s." % (task.executor.user.last_name+' '+task.executor.user.first_name[0], task.status)
            r = smsc.send_sms('7%s' % profile.phone, text, sender="arm_zayavki")
            if len(r) == 4:
                logger.debug(u'Исполнитель %s +7%s уведомлён о получении новой заявки по смс' % (profile.user.username, profile.phone))
            else:
                error = r[2]
                logger.debug(u'Система не смогла уведомить исполнителя %s +7%s по смс. Ошибка: %s' % profile.user.username, profile.phone, error)

        elif task.notification == type_notify.get(slug='email'):
            subject = "АРМ 'Заявки. Уведомление по поставленой задаче"
            message = "АРМ 'Заявки'. Поставленая задача %s сменила статус на %s." % (task.executor.user.last_name+' '+task.executor.user.first_name[0], task.status)
            recipient_email = profile.user.email
            send_mail(subject, message, EMAIL_HOST_USER, [recipient_email])

    except:
        logger.error(u'Система не смогла уведомить по задаче %s.' % task.id)


@login_required
@csrf_protect
def addget_materials(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    formset = MaterialsFormSet(queryset=CalcMaterialsWorks.objects.filter(calculation=calc_data).order_by('material'))

    if request.POST:
        formset = MaterialsFormSet(data=request.POST)
        for form in formset:
            if form.is_valid():
                if form.cleaned_data.get('material'):
                    if form.cleaned_data['quantity'] == 0:
                        CalcMaterialsWorks.objects.filter(id=form.instance.id).delete()
                    else:
                        cmw = form.cleaned_data.get('material')
                        new_calc = form.save(commit=False)
                        if form.cleaned_data['material_rent']:
                            mprice = 0
                            new_calc.material_price = mprice
                        else:
                            mprice = MaterialsWorks.objects.get(id=cmw.pk).material_price
                            new_calc.material_price = mprice
                        new_calc.material_total = mprice * form.cleaned_data['quantity']
                        new_calc.work_total = cmw.work_price * form.cleaned_data['quantity']
                        new_calc.save()

        return redirect('tasks:addget_params', calc_data.pk)

    return render(request, "materials.html", {
        'title': 'Ввод материала',
        'title_small': 'Работа с клиентом',
        'calc_data': calc_data,
        'form_fillmaterials': form_fill_materials,
        'formset': formset,
    })


@login_required
@csrf_protect
def fill_materials(request, calc_id):
    form = form_fill_materials(request.POST or None)

    if request.POST:
        if form.is_valid():
            set = form.cleaned_data.get('set')
            material_list = MaterialsWorks.objects.filter(set=set).order_by('name')
            for material in material_list:
                if set in material.rent_set.all():
                    summ = 0
                    rent = True
                else:
                    summ = material.material_price
                    rent = False
                CalcMaterialsWorks.objects.create(
                    calculation=Calculations.objects.get(id=calc_id),
                    material=material,
                    material_price=material.material_price, #summ,
                    work_price=material.work_price,
                    material_rent=False  #rent
                )

    return redirect('tasks:addget_materials', calc_id)


@login_required
@csrf_protect
def addget_params(request, calc_id):
    total_materials = total_works = total_sale = total_summ = total_worksale = commissioning_price = project_price = 0

    form = form_calc_additional_fields(request.POST or None, instance=calc_id and Calculations.objects.get(id=calc_id))

    if request.POST:
        if form.is_valid():
            form.save()

    calc_data = Calculations.objects.get(id=calc_id)
    calc_list = CalcMaterialsWorks.objects.filter(calculation=calc_data)
    if calc_list.count() > 0:
        total_materials = calc_list.aggregate(summ=Sum('material_total', output_field=FloatField()))
        total_works = calc_list.aggregate(summ=Sum('work_total', output_field=FloatField()))
        if calc_data.commissioning:
            commissioning_price = calc_data.commissioning.price
        if calc_data.projects:
            project_price = calc_data.projects.price
        total_sale = (calc_data.Sale/100)*(0 if total_works['summ'] is None else total_works['summ'])
        total_worksale = float(total_works['summ']) - total_sale
        total_summ = total_materials['summ'] + total_worksale + float(commissioning_price) + float(project_price)
        Calculations.objects.filter(id=calc_id).update(total_summ=round(total_summ, 2))

    return render(request, "additional_fields.html", {
        'title': 'Ввод дополнительных параметров',
        'title_small': 'Работа с клиентом',
        'calc_data': calc_data,
        'form': form,
        'total_materials': round((total_materials['summ'] if total_materials else 0), 2),
        'total_works': round((total_works['summ'] if total_works else 0), 2),
        'total_sale': round(total_sale, 2),
        'total_commissioning': commissioning_price,
        'total_project': project_price,
        'total_worksale': round(total_worksale, 2),
        'total_summ': round(total_summ, 2)
    })


@login_required
@csrf_protect
def print_calculations(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    calc_list = CalcMaterialsWorks.objects.filter(calculation=calc_data).order_by('material_rent')

    text_template = Template(TemplateDocuments.objects.get(slug='estimate').TextTemplate)

    m = 0
    text_materials = type_text = commissioning_row = project_row = sale_row = ''

    for item in calc_list:
        m = m + 1
        if item.material_price > 0:
            str_materials = '<tr><td style="width: 30%">' + item.material.name + '</td>' \
                            '<td style="width: 20%">' + item.material.model + '</td>' \
                            '<td style="width: 10%">' + str(item.quantity) + '</td>' \
                            '<td style="width: 20%">' + str(item.material_price) + '</td>' \
                            '<td style="width: 20%">' + str(item.material_total) + '</td></tr>'
        else:
            str_materials = '<tr><td>' + item.material.name + '</td>' \
                            '<td>' + item.material.model + '</td>' \
                            '<td>' + str(item.quantity) + '</td>' \
                            '<td colspan="2">' + str(item.material_price if item.material_price > 0 else 'Собственность ООО "ЧОП Амулет-ПЦО"') + '</td></tr>'

        text_materials = text_materials + str_materials

    for item in calc_data.TypeTask.all():
        if type_text == '':
            type_text = item.Name
        else:
            type_text = type_text + ', ' + item.Name

    total_materials = calc_list.aggregate(summ=Sum('material_total', output_field=FloatField()))
    total_works = calc_list.aggregate(summ=Sum('work_total', output_field=FloatField()))
    commissioning_price = float(0 if calc_data.commissioning is None else calc_data.commissioning.price)
    if commissioning_price > 0:
        commissioning_row = '<tr><th colspan="4" style="text-align:right">Пуско-наладочные работы на ' + calc_data.commissioning.name + ' канал:</th>' \
                            '<td style="text-align:center">' + str(commissioning_price) + '</td></tr>'

    project_price = float(0 if calc_data.projects is None else calc_data.projects.price)
    if project_price > 0:
        project_row = '<tr><th colspan="4" style="text-align:right">Проектные работы ' + calc_data.projects.name + ':</th>' \
                            '<td style="text-align:center">' + str(project_price) + '</td></tr>'
    total_sale = (calc_data.Sale / 100) * (0 if total_works['summ'] is None else total_works['summ'])
    if calc_data.Sale > 0:
        sale_row = '<tr><th colspan="4" style="text-align:right">Договорное снижение ' + str(calc_data.Sale) + '%:</th>' \
                        '<td style="text-align:center">' + str(round(total_sale, 2)) + '</td></tr>'

    text_additional = commissioning_row + project_row + sale_row

    total_worksale = float(total_works['summ']) - total_sale
    total_summ = total_materials['summ'] + total_worksale + commissioning_price + project_price

    tags = Context({
        'Type': type_text,
        'Materials': text_materials,
        'Address': calc_data.AddressObject,
        'totalsumm_materials': total_materials['summ'],
        'totalsumm_works': total_works['summ'],
        'additional_fields':  text_additional,
        'total_summ': total_summ,
    })

    return render(request, 'view_template.html', {
        'title': 'Печатная форма калькуляции ',
        'title_small': 'Работа с клиентом',
        'text': text_template.render(tags)
    })


@login_required()
@csrf_protect
def get_notify_calc(request, notify_id):
    calc_data = CalcNotify.objects.get(id=notify_id).calculation
    CalcNotify.objects.filter(id=notify_id).update(read=True, date_read=datetime.today())

    if calc_data.disposer:
        if calc_data.executor:
            if request.user == calc_data.executor.user:
                return redirect('tasks:calc_executor', calc_data.id)
            else:
                if request.user in User.objects.filter(groups__name='storekeepers'):
                    Calculations.objects.filter(id=calc_data.id).\
                        update(storekeeper=Profile.objects.get(user=request.user))
                if request.user in User.objects.filter(groups__name='accountants'):
                    Calculations.objects.filter(id=calc_data.id).\
                        update(accountant=Profile.objects.get(user=request.user))
                if request.user in User.objects.filter(groups__name='managers'):
                    Calculations.objects.filter(id=calc_data.id).\
                        update(manager=Profile.objects.get(user=request.user))
                return redirect('tasks:calc_other', calc_data.id)
        else:
            return redirect('tasks:calc_disposer', calc_data.id)
    return redirect('tasks:calc_disposer', calc_data.id)



@login_required
@csrf_protect
def print_workorder(request, calc_id):
    pass


@login_required
@csrf_protect
def print_actdelivery(request, calc_id):
    pass


def get_estimate(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    mf = magic.from_file(calc_data.Estimate.path, mime=True)
    file_path = os.path.join(settings.MEDIA_ROOT, calc_data.Estimate.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mf)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def get_actdelivery(request, calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    mf = magic.from_file(calc_data.Act_Delivery.path, mime=True)
    file_path = os.path.join(settings.MEDIA_ROOT, calc_data.Act_Delivery.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mf)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def task_notification_executor(task_id):
    smsc = SMSC()
    task = user_task.objects.get(id=task_id)

    try:
        text = "АРМ 'Заявки'. Вам поставлена задача %d до %s включительно." % (task_id, task.Date_limit.strftime("%d.%m.%Y"))
        r = smsc.send_sms('7%s' % task.executor.phone, text, sender="arm_zayavki")
        if len(r) == 4:
            logger.debug(u'Исполнитель %s +7%s уведомлён о получении задания №%d по смс' % (task.executor.user.username, task.executor.phone, task.id))
        else:
            error = r[2]
            logger.debug(u'Система не смогла уведомить исполнителя %s +7%s по смс. Ошибка: %s' % (task.executor.user.username, task.executor.phone, error))

    except:
        logger.error(u'Система не смогла уведомить по задаче %s.' % task.id)


@login_required()
@permission_required('tasks.task_list_view', login_url=reverse_lazy('page_error403'))
def getlist_tasks(request):
    list_groups = request.user.groups.all()
    qs = user_task.objects.filter(Q(executor__in=Profile.objects.filter(user=request.user))|
                                  Q(author=request.user)|Q(group_executor__in=list_groups))
    task_filter = tasks_filter(request.GET, queryset=qs)

    return render(request, 'tasks_list.html', {
        'title': u'Список задач',
        'title_area': u'Задачи',
        'tasks': qs,
        'task_filter': task_filter,
        'cur_date': datetime.today().date()
    })


def send_notify_telegram(data):
    url = "https://api.telegram.org/bot1730861248:AAH4B5r3YKhzONijjLKEyy8zIJleuO3Nk7s"
    if data.executor:
        text = "Для %s появилась задача: №%d.\nНаименование: %s. \nОписание: %s. \nСрок: до 18:00 %s" % (
            data.executor, data.id, data.title, data.description, data.Date_limit.__str__())
    else:
        list_fio = ''
        executors = User.objects.filter(groups__name=data.group_executor.name)
        for fio in executors:
            if list_fio:
                list_fio = list_fio + ', ' + view_shortfio_user(fio)
            else:
                list_fio = view_shortfio_user(fio)
        text = "%s\nДля %s появилась задача: №%d.\nНаименование: %s.\nОписание: %s.\nСрок: до 18:00 %s" % (
            data.group_executor.name, list_fio, data.id, data.title, data.description, data.Date_limit.__str__())

    params = {'chat_id': -1001422493774, 'text': text}
    requests.post(url + '/sendMessage', data=params)


@login_required()
@permission_required('tasks.task_item_view', login_url=reverse_lazy('page_error403'))
@csrf_protect
def addget_task(request, task_id=None):
    if task_id:
        task_data = user_task.objects.get(id=task_id)
    else:
        task_data = user_task.objects.none()

    form = form_add_task(request.POST or None, request.FILES or None, user=request.user,
                         instance=task_id and user_task.objects.get(id=task_id))

    if request.POST:
        if form.is_valid():
            old_data = user_task.objects.none()
            new_task = form.save(commit=False)

            if task_id:
                old_data = user_task.objects.get(id=task_id)
                if request.user != old_data.author:
                    new_task.title = old_data.title
                    new_task.description = old_data.description
                    new_task.executor = old_data.executor
                    new_task.Date_limit = old_data.Date_limit
                    new_task.high_importance = old_data.high_importance
                    new_task.notification = old_data.notification
                    if old_data.status != form.cleaned_data['status']:
                        new_task.read = False
                new_task.Update_user = request.user
            else:
                new_task.author = request.user
                new_task.Create_user = request.user
                new_task.status = Status_task.objects.get(slug='open')
            new_task.save()

            if old_data:
                if old_data.status != new_task.status:
                    if new_task.status.slug == 'complete':
                        task_notification_author(new_task.id)
            else:
                if new_task.status.slug == 'open':
                    send_notify_telegram(new_task)

            return redirect('tasks:getlist_tasks')
        else:
            return render(request, 'tasks_one.html', {
                'title': 'Задача №%s' % task_id,
                'title_small': 'Задачи',
                'form': form,
                'task_data': task_data
            })
    else:
        if task_id:
            task_data = user_task.objects.get(id=task_id)
            user_task.objects.filter(id=task_id).update(read=True)
        return render(request, 'tasks_one.html', {
            'title': 'Задача №%s' % task_id,
            'title_small': 'Задачи',
            'form': form,
            'task_data': task_data
        })


def get_file(request, task_id):
    task_data = user_task.objects.get(id=task_id)
    mf = magic.from_file(task_data.file.path, mime=True)
    file_path = os.path.join(settings.MEDIA_ROOT, task_data.file.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mf)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
