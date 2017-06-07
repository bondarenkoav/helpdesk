__author__ = 'ipman'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^transmitters/item/(?P<transmitter_id>\d+)/$', 'reference_books.views.get_new_save_transmitters_item'),
    url(r'^transmitters/item/None/$', 'reference_books.views.get_new_save_transmitters_item'),
    url(r'^transmitters/item/$', 'reference_books.views.get_new_save_transmitters_item'),
    url(r'^transmitters/$', 'reference_books.views.get_model_transmitters'),

    url(r'^routs/item/(?P<routes_id>\d+)/$', 'reference_books.views.get_add_routs_item'),
    url(r'^routs/item/None/$', 'reference_books.views.get_add_routs_item'),
    url(r'^routs/item/$', 'reference_books.views.get_add_routs_item'),
    url(r'^routs/$', 'reference_books.views.get_routs'),

    url(r'^clients/item/(?P<client_id>\d+)/$', 'reference_books.views.get_new_save_clients_item'),
    url(r'^clients/item/None/$', 'reference_books.views.get_new_save_clients_item'),
    url(r'^clients/item/$', 'reference_books.views.get_new_save_clients_item'),
    url(r'^clients/$', 'reference_books.views.get_clients'),

    url(r'^coworker/item/(?P<coworker_id>\d+)/$', 'reference_books.views.get_new_save_coworker_item'),
    url(r'^coworker/item/None/$', 'reference_books.views.get_new_save_coworker_item'),
    url(r'^coworker/item/$', 'reference_books.views.get_new_save_coworker_item'),
    url(r'^coworker/page/(?P<page_id>\d+)/$', 'reference_books.views.get_coworker'),
    url(r'^coworker/$', 'reference_books.views.get_coworker'),
)