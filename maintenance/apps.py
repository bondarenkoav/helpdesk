__author__ = 'ipman'

from django.apps import AppConfig

class MaintenanceAppConfig(AppConfig):
    name = "maintenance" # Здесь указываем исходное имя приложения
    verbose_name = "Техническое обслуживание" # А здесь, имя которое необходимо отобразить в админке