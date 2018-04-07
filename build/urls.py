__author__ = 'ipman'

from django.conf.urls import patterns, url
from build.views import *

urlpatterns = patterns('',
    url(r'^item/(?:id-(?P<request_id>\d+)/)?$', addget_request_build, name='add&get_request'),
    url(r'^(?P<status>\w+)/$', get_requests_build, name='get_requests'),

    url(r'^request/id-(?P<request_id>\d+)/acts/(?:id-(?P<act_id>\d+)/)?$', addget_act_build, name='add&get_act'),
    url(r'^request/acts/(?:page-(?P<page_id>\d+)/)?$', get_acts_build, name='get_acts'),

    # url(r'^item/(?:id-(?P<request_id>\d+)/)?$', get_new_save_request_build_item, name=''),
    #
    # url(r'^(?P<status>\w+)/(?:page-(?P<page_id>\d+)/)?$', get_requests_build, name=''),
    #
    # url(r'^(?P<request_id>\d+)/acts/item/(?:id-(?P<act_id>\d+)/)?$', 'build.views.get_new_save_acts_build_item'),
    # url(r'^(?P<request_id>\d+)/acts/item/None/$', 'build.views.get_new_save_acts_build_item'),
    #
    # url(r'^acts/page/(?P<page_id>\d+)/$', 'build.views.get_acts_build'),
    #
    # url(r'^coworkers_range_date/$', 'build.views.get_coworkers_range_date'),
    # url(r'^coworkers_object/$', 'build.views.get_coworkers_object'),
    # url(r'^coworker_range_date/$', 'build.views.get_coworker_range_date'),
    #
    # #url(r'^acts/$', 'build.views.get_acts_build'),
)