from django.contrib import admin

from .models import City, Posts, CoWorker, ServiceCompanies, Numerate, Client, TypeSecurity, \
    SystemPCN, ModelTransmitter, Send_mail_list, OpSoS_name, OpSoS_rate, Event, RoutesMaintenance, MaterialsWorks, \
    Measure, AdditionallyWorks, SetMaterials


class RoutesMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['Number', 'ServiceCompany', 'Descript']


class CoWorkerAdmin(admin.ModelAdmin):
    list_display = ['Person_FIO', 'Posts', 'location', 'StatusWorking']
    list_filter = ['Posts', 'StatusWorking', 'location']
    search_fields = ['Person_FIO']
    ordering = ['StatusWorking', 'Person_FIO']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['Name', 'City', 'slug']


class NumerateAdmin(admin.ModelAdmin):
    list_display = ['ServiceCompany', 'slug_model', 'last_num']


class TypeSecurityAdmin(admin.ModelAdmin):
    list_display = ['Name', 'slug']


class Send_mail_listAdmin(admin.ModelAdmin):
    list_display = ['GroupName', 'ServiceCompany', 'Subject']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']
    search_fields = ['Name']
    ordering = ['Name']


class OpSoSRateInline(admin.TabularInline):
    model = OpSoS_rate
    extra = 1


class OpSoSNameAdmin(admin.ModelAdmin):
    list_display = ['Name']
    inlines = [OpSoSRateInline]


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'slug', 'forfilter']
    search_fields = ['Name']
    ordering = ['Name']


class MaterialsWorksAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']


admin.site.register(SystemPCN)
admin.site.register(RoutesMaintenance, RoutesMaintenanceAdmin)
admin.site.register(Send_mail_list, Send_mail_listAdmin)
admin.site.register(Measure)
admin.site.register(SetMaterials)
admin.site.register(MaterialsWorks, MaterialsWorksAdmin)
admin.site.register(AdditionallyWorks)
admin.site.register(ModelTransmitter)
admin.site.register(City)
admin.site.register(ServiceCompanies, CompanyAdmin)
admin.site.register(Posts)
admin.site.register(Client, ClientAdmin)
admin.site.register(TypeSecurity, TypeSecurityAdmin)
admin.site.register(Numerate, NumerateAdmin)
admin.site.register(CoWorker, CoWorkerAdmin)
admin.site.register(OpSoS_name, OpSoSNameAdmin)
admin.site.register(Event, EventAdmin)
