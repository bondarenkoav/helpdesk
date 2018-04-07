__author__ = 'ipman'

from django.conf.urls import patterns, url
from claim.views import *

urlpatterns = patterns('',
    # Добавить, изменить заявку
    url(r'^item/(?:id-(?P<request_id>\d+)/)?$', addget_request_trouble_shooting, name='add&get_request'),
    # Список заявок с непредставленным актом
    #url(r'^act_required/(?:page-(?P<page_id>\d+)/)?$', get_requests_actrequired, name='get_requests_actrequred'),
    # Поиск и печать заявок c актами
    url(r'^act_required/$', get_requests_actrequired, name='get_request_actrequired_fordate'),
    # Вывести список заявок
    url(r'^(?P<status>\w+)/(?:page-(?P<page_id>\d+)/)?$', get_requests_trouble_shooting, name='get_requests'),
    url(r'^', get_requests_trouble_shooting),
)