__author__ = 'ipman'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^item/(?P<request_id>\d+)/object/(?P<object_id>\d+)/$', 'maintenance.views.get_new_save_request_item'),
    url(r'^item/None/object/(?P<object_id>\d+)/$', 'maintenance.views.get_new_save_request_item'),
    url(r'^item/$', 'maintenance.views.get_new_save_request_item'),

    url(r'^objects/item/(?P<object_id>\d+)/$', 'maintenance.views.get_add_object_to_item'),
    url(r'^objects/item/None/$', 'maintenance.views.get_add_object_to_item'),
    url(r'^objects/item/$', 'maintenance.views.get_add_object_to_item'),

    url(r'^objects_change_month/$', 'maintenance.views.get_requestTO_change_month'),

    url(r'^objects/page/(?P<page_id>\d+)/$', 'maintenance.views.get_objects_to_status'),
    url(r'^objects/$', 'maintenance.views.get_objects_to_status'),

    url(r'^trouble_shooting/item/(?P<request_id>\d+)/$', 'maintenance.views.get_add_trouble_shooting_item'),
    url(r'^trouble_shooting/item/None/$', 'maintenance.views.get_add_trouble_shooting_item'),
    url(r'^trouble_shooting/page/(?P<page_id>\d+)/$', 'maintenance.views.get_trouble_shooting'),
    url(r'^trouble_shooting/$', 'maintenance.views.get_trouble_shooting'),

    url(r'^create_to_request/$', 'maintenance.cron.cron_create_maintenance_request'),
    url(r'^close_request/$', 'maintenance.cron.cron_close_maintenance_object'),
    url(r'^email_send/$', 'maintenance.cron.cron_sendmail_maintenance_request'),

    url(r'^(?P<status>\w+)/page/(?P<page_id>\d+)/$', 'maintenance.views.get_requests_maintenance'),
    url(r'^(?P<status>\w+)/$', 'maintenance.views.get_requests_maintenance'),
)