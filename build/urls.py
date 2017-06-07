__author__ = 'ipman'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^item/(?P<request_id>\d+)/$', 'build.views.get_new_save_request_build_item'),
    url(r'^item/None/$', 'build.views.get_new_save_request_build_item'),
    url(r'^item/$', 'build.views.get_new_save_request_build_item'),

    url(r'^(?P<status>\w+)/page/(?P<page_id>\d+)/$', 'build.views.get_requests_build'),
    url(r'^(?P<status>\w+)/$', 'build.views.get_requests_build'),

    url(r'^(?P<request_id>\d+)/acts/item/(?P<act_id>\d+)/$', 'build.views.get_new_save_acts_build_item'),
    url(r'^(?P<request_id>\d+)/acts/item/None/$', 'build.views.get_new_save_acts_build_item'),

    url(r'^acts/page/(?P<page_id>\d+)/$', 'build.views.get_acts_build'),

    url(r'^coworkers_range_date/$', 'build.views.get_coworkers_range_date'),
    url(r'^coworkers_object/$', 'build.views.get_coworkers_object'),
    url(r'^coworker_range_date/$', 'build.views.get_coworker_range_date'),

    #url(r'^acts/$', 'build.views.get_acts_build'),
)