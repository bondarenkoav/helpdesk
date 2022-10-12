__author__ = 'ipman'

from django.conf.urls import url
from dashboard.views import search_requests, index

app_name = 'dashboard'

urlpatterns = [
    # Поиск и печать заявок
    url(r'^search/$', search_requests, name='search'),
    # График тестовый
    # url(r'^chart/$', , name='chart'),
    # Самая первая страница
    url(r'^', index, name='index'),
]