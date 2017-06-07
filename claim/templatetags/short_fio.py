from django.template.defaultfilters import stringfilter

__author__ = 'ipman'

from django import template

register = template.Library()

@register.filter
@stringfilter
def short_fio(value):
    full_name = value.split(' ')
    if full_name[0] != '' and full_name[1] != '':
        return full_name[0]+' '+full_name[1][:1]+'.'
    else:
        return full_name[0]