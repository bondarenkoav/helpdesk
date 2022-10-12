from django.conf.urls import url

from maintenance.cron import cron_create_maintenance_request_manual
from maintenance.views import addget_mproposals, addget_mobjects, addget_mtroubles, get_mobjects, \
    get_mproposals_on_routs, get_mtroubles, get_mproposals

__author__ = 'ipman'

app_name = 'maintenance'

urlpatterns = [
    url(r'^create_request_manual/', cron_create_maintenance_request_manual),
    # Открыть Добавить заявку на ТО
    url(r'^objects/id-(?P<object_id>\d+)/item/(?:id-(?P<proposal_id>\d+)/)?$',
        addget_mproposals, name='addget_mproposals'),
    # Открыть или добавить объект ТО
    url(r'^objects/(?:id-(?P<object_id>\d+)/)?$', addget_mobjects, name='addget_mobjects'),
    # Добавить заявку на устранение неисправности во время ТО
    url(r'^troubles/item/(?:id-(?P<trouble_id>\d+)/)?$', addget_mtroubles, name='addget_mtroubles'),
    # Вывести объекты ТО
    url(r'^objects-(?P<status>\w+)/$', get_mobjects, name='get_mobjects'),
    # Вывести объекты ТО на месяц
    url(r'^on_routes/$', get_mproposals_on_routs, name='get_mproposals_onrouts'),
    # Вывести заявки по неисправностям
    url(r'^troubles/$', get_mtroubles, name='get_mtroubles'),
    # Вывести заявки ТО
    url(r'^(?P<status>\w+)/$', get_mproposals, name='get_mproposals'),
]