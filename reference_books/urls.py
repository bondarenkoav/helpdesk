__author__ = 'ipman'

from django.conf.urls import url
from reference_books.views import *

urlpatterns = [
    url(r'^transmitters/item/(?P<transmitter_id>\d+)/$', get_add_transmitter, name='add&get_transmitter'),
    url(r'^transmitters/$', get_transmitters, name='get_transmitters'),

    url(r'^routs/item/(?P<routes_id>\d+)/$', get_add_rout, name='add&get_rout'),
    url(r'^routs/$', get_routs, name='get_transmitters'),

    url(r'^clients/item/(?P<client_id>\d+)/$', get_add_client, name='add&get_client'),
    url(r'^clients/(?:page-(?P<page_id>\d+)/)?$', get_clients, name='get_clients'),

    url(r'^coworker/item/(?P<coworker_id>\d+)/$', get_add_coworker, name='add&get_coworker'),
    url(r'^coworker/(?:page-(?P<page_id>\d+)/)?$', get_coworkers, name='get_coworkers'),
]