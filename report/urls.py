__author__ = 'ipman'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^coworkers_range_date/$', 'report.views.get_coworkers_range_date'),
    #url(r'^coworkers_object/$', 'report.views.get_coworkers_object'),
    #url(r'^coworker_range_date/$', 'report.views.get_coworker_range_date'),
)