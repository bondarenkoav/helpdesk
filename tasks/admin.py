from django.contrib import admin

from tasks.models import Calculations, CalcMaterialsWorks, TemplateDocuments, CalcNotify, CalcHistory, user_task


class CalcMaterialsWorksInline(admin.TabularInline):
    model = CalcMaterialsWorks
    extra = 0


class CalcNotifyInline(admin.TabularInline):
    model = CalcNotify
    extra = 0


class CalcHistoryInline(admin.TabularInline):
    model = CalcHistory
    extra = 0


class CalculationsAdmin(admin.ModelAdmin):
    list_display = ['AddressObject', 'operator', 'disposer', 'executor', 'manager', 'accountant', 'storekeeper',
                    'Status']
    list_filter = ['executor']
    search_fields = ['AddressObject']
    #inlines = [CalcMaterialsWorksInline, CalcNotifyInline]
    model = Calculations


admin.site.register(user_task)
admin.site.register(Calculations)#, CalculationsAdmin)
admin.site.register(TemplateDocuments)