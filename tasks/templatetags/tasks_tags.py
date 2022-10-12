from django import template

from tasks.models import Calculations

__author__ = 'ipman'


register = template.Library()


@register.simple_tag()
def get_url(calc_id):
    calc_data = Calculations.objects.get(id=calc_id)
    if calc_data.Status.slug == 'open':
        url = 'tasks:calc_disposer'
    else:
        url = 'tasks:calc_executor'
