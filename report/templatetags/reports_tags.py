from django import template

from build.models import bacts, bproposals
from exploitation.models import eproposals
from maintenance.models import mproposals, mobjects
from reference_books.models import Status

__author__ = 'ipman'

register = template.Library()


@register.inclusion_tag('templatetags/employment_coworker_tags.html')
def get_employment_coworker(coworker, date_start, date_end, scompany):
    list_build = bacts.objects.\
        filter(CoWorkers=coworker,
               proposal__in=bproposals.objects.filter(ServiceCompany=scompany),
               Day_reporting__range=(date_start, date_end)).\
        order_by('Day_reporting')
    list_exploitation = eproposals.objects.\
        filter(CoWorkers=coworker, ServiceCompany=scompany,
               DateTime_work__range=(date_start, date_end),
               Status=Status.objects.get(slug='close')).\
        order_by('DateTime_work')
    list_maintenance = mproposals.objects.\
        filter(CoWorkers=coworker,
               Object__in=mobjects.objects.filter(ServiceCompany=scompany),
               DateTime_work__range=(date_start, date_end),
               Status=Status.objects.get(slug='close')).\
        order_by('DateTime_work')

    return {'coworker': coworker, 'list_build': list_build, 'list_exploitation': list_exploitation,
            'list_maintenance': list_maintenance, 'date_start': date_start, 'date_end': date_end}


@register.inclusion_tag('templatetags/employment_date_tags.html')
def get_employment_dates(date, scompany):
    list_build = bacts.objects.\
        filter(Day_reporting=date,
               proposal__in=bproposals.objects.filter(ServiceCompany=scompany))
    list_exploitation = eproposals.objects.\
        filter(DateTime_work=date,
               Status=Status.objects.get(slug='close'),
               ServiceCompany=scompany)
    list_maintenance = mproposals.objects.\
        filter(DateTime_work=date,
               Status=Status.objects.get(slug='close'),
               Object__in=mobjects.objects.filter(ServiceCompany=scompany))

    return {'date': date, 'list_build': list_build, 'list_exploitation': list_exploitation,
            'list_maintenance': list_maintenance}