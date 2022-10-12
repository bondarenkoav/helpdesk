__author__ = 'ipman'

from django.apps import AppConfig

class AccountsAppConfig(AppConfig):
    name = "accounts" # Здесь указываем исходное имя приложения
    verbose_name = "Профили пользователей" # А здесь, имя которое необходимо отобразить в админке