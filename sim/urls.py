__author__ = 'ipman'

from django.conf.urls import patterns, url
from sim.views import *
from report import views as report_views

urlpatterns = patterns('',
    # Карточка симкарты
    url(r'^item/(?:id-(?P<simcard_id>\d+)/)?$', get_new_simcard_item, name='add&get_simcard'),
    # Список симкарт
    url(r'^(?P<status>\w+)/$', get_simcard_list, name='getlist_simcard'),
    # Журнал изменений
    url(r'^jornal_change/$', report_views.get_jornal_changes, name='journal_changes'),
)