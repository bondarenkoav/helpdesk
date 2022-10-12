__author__ = 'ipman'

from django.conf.urls import url
from reference_books.views import addget_pcn, get_pcn, addget_transmitter, get_transmitters, addget_rout, get_routs, \
    addget_client, get_clients, addget_coworker, get_coworkers, addget_opsosname, get_opsosnames, addget_opsosrate, \
    get_opsosrates

app_name = 'reference_books'

urlpatterns = [
    url(r'^pcn/item/(?:(?P<pcn_id>\d+)/)?$', addget_pcn, name='addget_pcn'),
    url(r'^pcn/$', get_pcn, name='get_pcn'),

    url(r'^transmitters/item/(?:(?P<transmitter_id>\d+)/)?$', addget_transmitter, name='addget_transmitter'),
    url(r'^transmitters/$', get_transmitters, name='get_transmitters'),

    url(r'^routs/item/(?:(?P<routes_id>\d+)/)?$', addget_rout, name='addget_rout'),
    url(r'^routs/$', get_routs, name='get_routs'),

    url(r'^clients/item/(?:(?P<client_id>\d+)/)?$', addget_client, name='addget_client'),
    url(r'^clients/$', get_clients, name='get_clients'),

    url(r'^coworkers/item/(?:(?P<coworker_id>\d+)/)?$', addget_coworker, name='addget_coworker'),
    url(r'^coworkers/$', get_coworkers, name='get_coworkers'),

    url(r'^opsosnames/item/(?:(?P<name_id>\d+)/)?$', addget_opsosname, name='addget_opsosname'),
    url(r'^opsosnames/$', get_opsosnames, name='get_opsosnames'),

    url(r'^opsosrates/item/(?:(?P<rate_id>\d+)/)?$', addget_opsosrate, name='addget_opsosrate'),
    url(r'^opsosrates/$', get_opsosrates, name='get_opsosrates'),
]