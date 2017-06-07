from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Status, support_request, TypeRequest,  CategoryMenu

class support_requestAdmin(admin.ModelAdmin):
    list_display = ['id','Company','NumObject','AddressObject','DateTime_add','DateTime_update','DescriptionWorks','Status']
    list_filter = ['DateTime_add','Status']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['Name','slug','tr_color']

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

#admin.site.register(CategoryMenu, MPTTModelAdmin)
admin.site.register(CategoryMenu, DraggableMPTTAdmin)

admin.site.register(TypeRequest)
admin.site.register(Status, StatusAdmin)
admin.site.register(support_request, support_requestAdmin)