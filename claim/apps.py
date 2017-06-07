__author__ = 'ipman'

from django.apps import AppConfig

class ClaimAppConfig(AppConfig):
    name = "claim" # Здесь указываем исходное имя приложения
    verbose_name = "Заявки" # А здесь, имя которое необходимо отобразить в админке