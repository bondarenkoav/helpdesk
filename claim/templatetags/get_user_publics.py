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