__author__ = 'ipman'

from django.conf.urls import url
from sim.views import get_new_simcard_item, get_simcard_list, get_simcard_archive_list, parseExcel

app_name = 'simmanage'

urlpatterns = [
    # Карточка симкарты
    url(r'^item/(?:id-(?P<simcard_id>\d+)/)?$', get_new_simcard_item, name='addget_simcard'),
    # Список архива
    url(r'^archive/', get_simcard_archive_list, name='getlist_simcard_archive'),
    # Список симкарт
    url(r'^active/', get_simcard_list, name='getlist_simcard'),
    # Парсинг Excel-файла
    url(r'^import_sim/', parseExcel, name='import_sim'),
]