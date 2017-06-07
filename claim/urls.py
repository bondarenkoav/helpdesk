__author__ = 'ipman'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<status>\w+)/page/(?P<page_id>\d+)/$', 'claim.views.get_requests_trouble_shooting'),
    url(r'^item/(?P<request_id>\d+)/$', 'claim.views.get_new_save_request_item'),
    url(r'^item/None/$', 'claim.views.get_new_save_request_item'),
    url(r'^item/$', 'claim.views.get_new_save_request_item'),
    url(r'^date/$', 'claim.views.get_requests_per_date'),

    url(r'^(?P<status>\w+)/$', 'claim.views.get_requests_trouble_shooting'),

    url(r'^', 'claim.views.get_requests_trouble_shooting'),
)