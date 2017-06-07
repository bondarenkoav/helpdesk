from django.contrib import admin

# Register your models here.
from .models import City, Posts, ExpandedUserProfile, CoWorker, Company, Numerate, Month_list, Client, TypeSecurity, \
    SystemPCN, ModelTransmitter, Send_mail_list, OpSoS_name, OpSoS_rate, Event


class ExpandedUserProfileAdmin(admin.ModelAdmin):
    list_display = ['Name','UserName','ServingCompany']

class CoWorkerAdmin(admin.ModelAdmin):
    list_display = ['Person_FIO','Posts','ServingCompany']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['Name','City','slug']

class NumerateAdmin(admin.ModelAdmin):
    list_display = ['ServingCompany','slug_model','last_num']

class TypeSecurityAdmin(admin.ModelAdmin):
    list_display = ['Name','slug']

class Send_mail_listAdmin(admin.ModelAdmin):
    list_display = ['GroupName','ServingCompany','Subject']

class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','Name']
    search_fields = ['Name']
    ordering = ['Name']

class OpSoSRateInline(admin.TabularInline):
    model = OpSoS_rate
    extra = 1

class OpSoSNameAdmin(admin.ModelAdmin):
    list_display = ['Name']
    inlines = [OpSoSRateInline]

class EventAdmin(admin.ModelAdmin):
    list_display = ['Name','slug']
    search_fields = ['Name']
    ordering = ['Name']

admin.site.register(SystemPCN)
admin.site.register(Send_mail_list,Send_mail_listAdmin)
admin.site.register(ModelTransmitter)
admin.site.register(City)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Posts)
admin.site.register(Client,ClientAdmin)
admin.site.register(TypeSecurity,TypeSecurityAdmin)
admin.site.register(Numerate,NumerateAdmin)
admin.site.register(CoWorker, CoWorkerAdmin)
admin.site.register(ExpandedUserProfile, ExpandedUserProfileAdmin)
admin.site.register(OpSoS_name, OpSoSNameAdmin)
admin.site.register(Event, EventAdmin)