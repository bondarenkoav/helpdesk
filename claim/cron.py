import datetime, calendar
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template import Context, Template
from claim.models import support_request, TypeRequest, Status
from maintenance.models import objects_to
from reference_books.models import Numerate, Company, Send_mail_list, ExpandedUserProfile

__author__ = 'ipman'

def cron_close_maintenance_request(request):

    now_date = datetime.date.today()
    cur_month = now_date.month
    status_open = Status.objects.get(slug='open').id
    #status_close = Status.objects.get(slug='close').id

    objects_to.objects.filter(Date_close__lt=now_date,Status=status_open).update(Status=2)

    return HttpResponseRedirect('/')

def cron_create_maintenance_request(request):

    now_date = datetime.date.today()
    cur_month = now_date.month

    get_objects_cur_month = objects_to.objects.filter(Month_schedule=cur_month)

    for object in get_objects_cur_month:
        Company = object.ServingCompany

        last_num_request = Numerate.objects.get(ServingCompany=Company,slug_model='maintenance').last_num
        last_num_request = last_num_request + 1

        type_list = ''
        for type in object.TypeSecurity.all():
            type_list = type_list+', '+type.__str__()

        p = support_request(
            custom_id         = last_num_request,
            TypeRequest       = TypeRequest.objects.get(id=2),        #
            NumObject         = object.NumObject,
            AddressObject     = object.AddressObject,
            Client            = object.Client,
            Company           = object.ServingCompany,
            Create_user       = object.Create_user,
            FaultAppearance   = 'Плановое техническое обслуживание '+type_list+'.\nЗаявка создана автоматически системой.',
            DateTime_schedule = now_date,
            other_app_id      = object.id
        )
        p.save(force_insert=True)

        Numerate.objects.filter(ServingCompany=Company,slug_model='maintenance').update(last_num=last_num_request)

    return HttpResponseRedirect('/')

def cron_sendmail_maintenance_request(request):

    get_sendmail_list = Send_mail_list.objects.all()                #
    type_id     = TypeRequest.objects.get(slug='maintenance').id
    status_id   = Status.objects.get(slug='open').id

    for setting in get_sendmail_list:
        now_date = datetime.date.today()
        cur_day = now_date.day
        cur_month = now_date.month
        count_day_cur_month = calendar.mdays[datetime.date.today().month]

        list_request = support_request.objects.filter(Company=setting.ServingCompany,TypeRequest=type_id,Status=status_id,DateTime_schedule__lte=datetime.date(now_date.year,cur_month,count_day_cur_month))

        text_template = Template(setting.Subject)
        list_subject = Context({'destination': setting.Subject})
        subject = text_template.render(list_subject)

        text_template = Template(setting.Message)
        list_object = Context({'object': setting.objects})
        message = text_template.render(list_object)

        send_mail(subject,message,setting.EmailAddress)
