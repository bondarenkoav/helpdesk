from django.contrib import admin
from maintenance.models import mobjects, mproposals


class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['Object', 'DateTime_schedule', 'DateTime_work', 'DateTime_add']
    list_filter = ['DateTime_schedule', 'DateTime_work', 'Status', 'CoWorkers']


class ObjectTOAdmin(admin.ModelAdmin):
    list_display = ['NumObject', 'AddressObject', 'DateTime_add', 'Client_choices', 'ServiceCompany']
    list_filter = ['DateTime_add', 'ServiceCompany', 'Month_schedule', 'Status_object']



admin.site.register(mobjects, ObjectTOAdmin)
admin.site.register(mproposals, MaintenanceRequestAdmin)
