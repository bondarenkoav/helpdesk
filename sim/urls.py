__author__ = 'ipman'

from django.conf.urls import patterns, url
from sim import views as sim_views
from report import views as report_views

urlpatterns = patterns('',
    url(r'^page/(?P<page_id>\d+)/$', sim_views.get_simcard_list),
    url(r'^jornal_change/$', report_views.get_jornal_changes),

    url(r'^(?P<status>\w+)/page/(?P<page_id>\d+)/$', sim_views.get_simcard_list),
    url(r'^item/(?P<simcard_id>\d+)/$', sim_views.get_new_simcard_item),
    url(r'^item/None/$', sim_views.get_new_simcard_item),

    url(r'^(?P<status>\w+)/$', sim_views.get_simcard_list),

)