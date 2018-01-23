from maintenance.models import objects_to, Status_object

__author__ = 'ipman'

from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_user_publics(value):
    if value:
        name = User.objects.get(id=value)
        return name.last_name+' '+name.first_name[:1]+'.'
    else:
        return 'нет'

@register.inclusion_tag('templatetags/get_objects_to_curmonth.html')
def get_objects_to_curmonth(month_number,rout_id):
    objects = objects_to.objects.filter(Status=Status_object.objects.get(slug='open').id, Month_schedule=month_number,Routes=rout_id)
    return {'objects': objects}