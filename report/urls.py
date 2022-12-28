from django.conf.urls import url
from django.urls import path

from report.views import get_coworkers_range_date, kanban

__author__ = 'ipman'

app_name = 'reports'

urlpatterns = [
    path('coworkers_range_date/', get_coworkers_range_date, name='coworkers-range-date'),
    path('kanban/', kanban, name='kanban'),
]