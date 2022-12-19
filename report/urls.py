from django.conf.urls import url
from report.views import get_coworkers_range_date, kanban

__author__ = 'ipman'

app_name = 'reports'

urlpatterns = [
    url(r'^coworkers_range_date/$', get_coworkers_range_date, name='coworkers-range-date'),
    url(r'^kanban/$', kanban, name='kanban'),
]