__author__ = 'ipman'

from django.conf.urls import url
from report.views import *

urlpatterns = [
    url(r'^coworkers_range_date/$', get_coworkers_range_date, name='report_coworkers_range_date'),
]