__author__ = 'ipman'

import datetime
import calendar

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template import Context, Template
from django.utils.safestring import mark_safe
from helpdesk.settings import EMAIL_HOST_USER

from maintenance.models import mobjects, mproposals
from reference_books.models import ServiceCompanies, Send_mail_list, Status, TypeRequest, TypeDocument


# Автоматическое снятие объектов с ТО
def cron_close_maintenance_object():
    now_date = datetime.date.today()
    objects = mobjects.objects.filter(Date_end__lt=now_date, Status_object=True)
    objects.update(Status_object=False)


# Создаёт заявки 1 числа каждого месяца
def cron_create_maintenance_request():
    now_date = datetime.date.today()
    # cur_month = now_date.month
    get_objects_cur_month = mobjects.objects.filter(Month_schedule=now_date.month, Status_object=True)

    for object_item in get_objects_cur_month:
        mproposals.objects.create(
            TypeRequest=TypeRequest.objects.get(slug='maintenance'),
            TypeDocument=TypeDocument.objects.get(slug='request'),
            Object=object_item, DateTime_schedule=now_date, Create_user=User.objects.get(username='system')
        )


# Создаёт заявки 1го числа каждого месяца вручную
def cron_create_maintenance_request_manual(request):
    now_date = datetime.date.today()
    cur_month = now_date.month
    get_objects_cur_month = mobjects.objects.filter(Month_schedule=cur_month, Status_object=True)

    for object_item in get_objects_cur_month:
        mproposals.objects.create(
            TypeRequest=TypeRequest.objects.get(slug='maintenance'),
            TypeDocument=TypeDocument.objects.get(slug='request'),
            Object=object_item, DateTime_schedule=now_date, Create_user=User.objects.get(username='system')
        )
    return redirect('dashboard:index')


# Напоминает о не закрытых заявках 20,25-31 число каждого месяца
def cron_sendmail_maintenance_request():
    status_id = Status.objects.get(slug='open').id

    # Запрашиваем список сервисных компаний
    for company in ServiceCompanies.objects.all():
        # Запрашиваем список получателей одной компании
        for recipient in Send_mail_list.objects.filter(ServiceCompany=company.id):

            recipient_list = ''
            # Сформировали список получателей
            for item in recipient.Destination.all():
                if recipient_list == '':
                    recipient_list = item.__str__()
                else:
                    recipient_list = recipient_list+', '+item.__str__()
            # Получили текущую дату
            now_date = datetime.date.today()
            # Получили текущий месяц
            cur_month = now_date.month
            # Получили количество дней в месяце
            count_day_cur_month = calendar.mdays[datetime.date.today().month]
            # Получили список объектов
            list_object = mobjects.objects.filter(ServiceCompany=company.id)
            list_request = mproposals.objects.\
                filter(Object=list_object, Status=status_id,
                       DateTime_schedule__lte=datetime.date(now_date.year, cur_month, count_day_cur_month))

            i = 0
            request_list = ''

            # Сформировали список объектов
            for item in list_request:
                i = i+1
                object_data = i.__str__()+'. '+item.Object.Client.Name.__str__()+' ('+item.Object.AddressObject.__str__()+'),<br/>'
                if request_list == '':
                    request_list = object_data
                else:
                    request_list = request_list+object_data

            text_template = Template(recipient.Subject)

            subject = text_template.render(Context({'destination': recipient_list}))
            text_template = Template(recipient.Message)

            message = text_template.render(Context({'object': mark_safe(request_list)}))

            recipient_email = recipient.EmailAddress
            send_mail(subject, message, EMAIL_HOST_USER, [recipient_email])

    return redirect('dashboard:index')
