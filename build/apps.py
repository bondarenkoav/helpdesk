__author__ = 'ipman'

from django.apps import AppConfig

class BuildAppConfig(AppConfig):
    name = "build" # Здесь указываем исходное имя приложения
    verbose_name = "Монтаж" # А здесь, имя которое необходимо отобразить в админке