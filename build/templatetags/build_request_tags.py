__author__ = 'ipman'

from django import template
from build.models import bacts


register = template.Library()

@register.inclusion_tag('templatetags/bacts_coworker_tag.html')
def get_coworker_from_acts(item):
    query = bacts.objects.filter(proposal=item)
    return {'acts': query}
