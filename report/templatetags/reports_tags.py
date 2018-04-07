__author__ = 'ipman'

from django import template
from build.models import acts_build
from claim.models import support_request
from maintenance.models import maintenance_request
from reference_books.models import CoWorker, Status

register = template.Library()

@register.inclusion_tag('templatetags/employment_coworker_tags.html')
def get_employment_coworker(coworker,date_start,date_end):
    list_build = acts_build.objects.filter(CoWorkers=coworker,Day_reporting__range=(date_start, date_end)).order_by('Day_reporting')
    list_trouble = support_request.objects.filter(CoWorkers=coworker,DateTime_work__range=(date_start, date_end),Status=Status.objects.get(slug='complete')).order_by('DateTime_work')
    list_maintenance = maintenance_request.objects.filter(CoWorkers=coworker,DateTime_work__range=(date_start, date_end),Status=Status.objects.get(slug='complete')).order_by('DateTime_work')

    return {'coworker':coworker,'list_build':list_build,'list_trouble':list_trouble,'list_maintenance':list_maintenance}