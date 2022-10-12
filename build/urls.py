__author__ = 'ipman'

from django.conf.urls import url
from build.views import addget_bacts, addget_bproposals, get_bproposals, get_bacts

app_name = 'build'


urlpatterns = [
    url(r'^item/(?:id-(?P<proposal_id>\d+)/)?$', addget_bproposals, name='addget_bproposals'),

    url(r'^(?P<status>\w+)/$', get_bproposals, name='get_bproposals'),

    url(r'^proposal/id-(?P<proposal_id>\d+)/acts/(?:id-(?P<act_id>\d+)/)?$', addget_bacts, name='addget_bact'),
    url(r'^proposal/acts/(?:page=(?P<page_id>\d+)/)?$', get_bacts, name='get_bact'),
]