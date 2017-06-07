import datetime, calendar
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template import Context, Template
from maintenance.models import objects_to, maintenance_request, Status_object
from reference_books.models import Numerate, Company, Send_mail_list, ExpandedUserProfile, Status
from request.settings import EMAIL_HOST_USER
from django.utils.safestring import mark_safe

__author__ = 'ipman'

def cron_close_maintenance_object():            # Автоматическое снятие объектов с ТО

    now_date = datetime.date.today()
    cur_month = now_date.month
    status_open = Status.objects.get(slug='open').id

    objects_to.objects.filter(Date_close__lt=now_date,Status=status_open).update(Status=2)

#    return HttpResponseRedirect('/')

def cron_create_maintenance_request(request):           # Создаёт заявки 1 числа каждого месяца

    now_date = datetime.date.today()
    cur_month = now_date.month
    status_open = Status_object.objects.get(slug='open').id
    get_objects_cur_month = objects_to.objects.filter(Month_schedule=cur_month, Status=status_open)

    for object in get_objects_cur_month:
        object_id = objects_to.objects.get(id=object.id)
        type_list = ''
        for type in object.TypeSecurity.all():
            if type_list == '':
                type_list = type.__str__()
            else:
                type_list = type_list+', '+type.__str__()

        p = maintenance_request(
            Object            = object_id,
            TypeSecurity      = type_list,
            Create_user       = object.Create_user,
            DateTime_schedule = now_date
        )
        p.save(force_insert=True)

    return HttpResponseRedirect('/')

def cron_sendmail_maintenance_request():         # Напоминает о не закрытых заявках 20,25-31 число каждого месяца
    args = {}
    status_id = Status.objects.get(slug='open').id

    for company in Company.objects.all():                                               # Запрашиваем список сервисных компаний
        for recipient in Send_mail_list.objects.filter(ServingCompany=company.id):      # Запрашиваем список получателей одной компании

            recipient_list = ''
            for item in recipient.Destination.all():                                    # Сформировали список получателей
                if recipient_list == '':
                    recipient_list = item.__str__()
                else:
                    recipient_list = recipient_list+', '+item.__str__()

            now_date = datetime.date.today()                                            # Получили текущую дату
            cur_month = now_date.month                                                  # Получили текущий месяц
            count_day_cur_month = calendar.mdays[datetime.date.today().month]           # Получили количество дней в месяце
            list_object = objects_to.objects.filter(ServingCompany=company.id)          # Получили список объектов
            list_request = maintenance_request.objects.filter(Object=list_object,Status=status_id,DateTime_schedule__lte=datetime.date(now_date.year,cur_month,count_day_cur_month))

            i = 0
            request_list = ''
            for item in list_request:                                                   # Сформировали список объектов
                i = i +1
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
            send_mail(subject,message, EMAIL_HOST_USER, [recipient_email])

#    send_mail(subject,message, EMAIL_HOST_USER, [recipient_list])
#    return HttpResponseRedirect('/')