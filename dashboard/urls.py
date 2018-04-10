__author__ = 'ipman'

from django.conf.urls import url
from dashboard.views import *

urlpatterns = [
    # Поиск и печать заявок
    url(r'^search/$', search_requests, name='search'),
    # Самая первая страница
    url(r'^', index, name='index'),
]