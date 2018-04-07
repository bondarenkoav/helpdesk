from build.models import acts_build, build_request
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

@register.filter
def get_coworkers_build(value):
    list_cowork = ''
    req = build_request.objects.get(id=int(value))
    acts = acts_build.objects.filter(build_request=req)
    for act in acts:
        for cowork in act.CoWorkers.all():
            full_name = cowork.Person_FIO.split(' ')
            if full_name[0] != '' and full_name[1] != '':
                name_short = full_name[0]+' '+full_name[1][:1]+'.'
            else:
                name_short = full_name[0]
            if list_cowork.find(name_short)==-1:
                if list_cowork != '':
                    list_cowork = list_cowork+', '+name_short
                else:
                    list_cowork = name_short
    return list_cowork