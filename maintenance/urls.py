__author__ = 'ipman'

from maintenance.views import *
from django.conf.urls import url

urlpatterns = [
    # Добавить заявку на ТО
    url(r'^object/(?P<object_id>\d+)/item/(?:id-(?P<request_id>\d+)/)?$', addget_request_maintenance, name='add&get_request'),
    # Добавить объект ТО
    url(r'^objects/item/(?:id-(?P<object_id>\d+)/)?$', addget_object_maintenance, name='add&get_object'),
    # Вывести объекты ТО на месяц
    url(r'^objects_changemonth/$', get_requests_maintenance_change_month, name='get_requests_change_month'),
    # Вывести объекты ТО
    url(r'^objects/$', get_objects_maintenance, name='get_objects'),
    # Добавить заявку на устранение неисправности во время ТО
    url(r'^trouble/item/(?:id-(?P<request_id>\d+)/)?$', addget_trouble_shooting_item, name='add&get_trouble_request'),
    # Вывести заявки по неисправностям
    url(r'^trouble/(?:page-(?P<page_id>\d+)/)?$', get_trouble_shooting, name='get_troubles'),
    # Вывести заявки ТО
    #url(r'^(?P<status>\w+)/(?:page-(?P<page_id>\d+)/)?$', get_requests_maintenance, name='get_requests'),
    url(r'^(?P<status>\w+)/$', get_requests_maintenance, name='get_requests'),

    # url(r'^actrequired/(?:page-(?P<page_id>\d+)/)?$', get_requests_maintenance, name='get_requests_actrequired'),
    # url(r'^create_to_request/$', 'maintenance.
    # cron.cron_create_maintenance_request'),
    # url(r'^close_request/$', 'maintenance.cron.cron_close_maintenance_object'),
    # url(r'^email_send/$', 'maintenance.cron.cron_sendmail_maintenance_request'),
]