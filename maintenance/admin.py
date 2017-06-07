from django.contrib import admin

# Register your models here.
from maintenance.models import  objects_to, maintenance_request # Status_object,

class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['Object','DateTime_schedule','DateTime_work','Status','DateTime_add']

class Status_objectAdmin(admin.ModelAdmin):
    list_display = ['Name','slug']

class ObjectTOAdmin(admin.ModelAdmin):
    list_display = ['NumObject','AddressObject','DateTime_add','Status','Client','ServingCompany']
    list_filter = ['DateTime_add','Status']

#admin.site.register(Status_object, Status_objectAdmin)
admin.site.register(objects_to, ObjectTOAdmin)
admin.site.register(maintenance_request, MaintenanceRequestAdmin)