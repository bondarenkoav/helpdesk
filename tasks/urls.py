__author__ = 'ipman'

from django.conf.urls import url

from tasks.views import getlist_tasks, addget_task, get_file, calc_operator, calc_disposer, calc_executor, \
    addget_materials, addget_params, print_workorder, print_actdelivery, print_calculations, get_estimate, calc_other, \
    get_notify_calc, fill_materials, getlist_calc

app_name = 'tasks'

urlpatterns = [
    url(r'^add_calculations/$', calc_operator, name='calc_operator'),
    url(r'^calculations/$', getlist_calc, name='calculations'),
    url(r'^calc/disposer/(?P<calc_id>\d+)/$', calc_disposer, name='calc_disposer'),
    url(r'^calc/executor/(?P<calc_id>\d+)/$', calc_executor, name='calc_executor'),
    url(r'^calc/other/(?P<calc_id>\d+)/$', calc_other, name='calc_other'),

    # Ввод материалов, работ калькуляции
    url(r'^calc/(?P<calc_id>\d+)/materials/$', addget_materials, name='addget_materials'),
    url(r'^calc/(?P<calc_id>\d+)/fillmaterials/$', fill_materials, name='fill_materials'),
    url(r'^calc/(?P<calc_id>\d+)/additionparams/$', addget_params, name='addget_params'),

    # Печать калькуляции, заказ-наряда и акта приёмо-сдачи
    url(r'^calc/(?P<calc_id>\d+)/print/calculations/$', print_calculations, name='print_calculations'),
    url(r'^calc/(?P<calc_id>\d+)/print/workorder/$', print_workorder, name='print_workorder'),
    url(r'^calc/(?P<calc_id>\d+)/print/actdelivery/$', print_actdelivery, name='print_actdelivery'),

    # Скачивание файлов
    url(r'^calc/get_estimate/(?P<calc_id>\w+)/$', get_estimate, name='get_estimate'),
    #url(r'^calc/get_actdelivery/(?P<calc_id>\w+)/$', get_actdelivery, name='get_actdelivery'),
    #url(r'^calc/get_workorder/(?P<calc_id>\w+)/$', get_workorder, name='get_workorder'),
    url(r'^task/get_file/(?P<task_id>\w+)/$', get_file, name='get_file'),

    url(r'^notify/(?:id-(?P<notify_id>\d+)/)?$', get_notify_calc, name='get_notify_calc'),
    url(r'^task/(?:id-(?P<task_id>\d+)/)?$', addget_task, name='addget_task'),
    url(r'^', getlist_tasks, name='getlist_tasks'),
]