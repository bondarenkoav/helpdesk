from reference_books.models import Client

__author__ = 'ipman'

from maintenance.models import mobjects
from django import template

register = template.Library()


@register.inclusion_tag('rb_pagination.html')
def generate_pagination():
    return {'users': 'user'}


@register.inclusion_tag('templatetags/objects_to.html')
def get_objectto_list(rout_id):
    return {'objects': mobjects.objects.filter(Routes=rout_id)}


# Вывод наименования клиента
@register.simple_tag()
def get_clientname(client_id):
    client = Client.objects.get(id=client_id)
    return client.TypesClient.short_name + ' ' + client.Name
