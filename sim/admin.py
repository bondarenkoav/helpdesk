from django.contrib import admin
from sim.models import OpSoS_card


class OpSoS_cardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields': ['ServiceCompany', 'Status', 'archive']}),
        (u'Договор', {'fields': ['Contract', 'Contract_date', 'PersonalAccount',], 'classes': ['collapse']}),
        (u'Данные SIM', {'fields': ['OpSoSRate', 'Number_SIM', 'ICC_SIM'], 'classes': ['collapse']}),
        (u'Используется', {'fields': ['Use_type', 'Use_nameobject', 'Use_numberobject', 'Use_addressobject', 'Use_user'], 'classes': ['collapse']}),
        (u'Дополнительно', {'fields': ['Notation']}),
        #(u'История', {'fields': [ 'DateTime_add', 'DateTime_update', 'Create_user', 'Update_user'], 'classes': ['collapse']}),
    ]
    list_display = ['Number_SIM', 'OpSoSRate', 'Use_type', 'Use_nameobject', 'Use_numberobject', 'Use_addressobject', 'Use_user', 'Status']
    list_filter = ['ServiceCompany','Use_type','Status']


admin.site.register(OpSoS_card, OpSoS_cardAdmin)
