from django.contrib import admin
from build.models import bacts, bproposals


class ActsBuildInline(admin.StackedInline):
    model = bacts
    extra = 1


class ProposalBuildAdmin(admin.ModelAdmin):
    list_display = ['Client_choices', 'AddressObject', 'ServiceCompany', 'Status']
    list_filter = ['ServiceCompany', 'Status']
    inlines = [ActsBuildInline]


class TypeBuildAdmin(admin.ModelAdmin):
    list_display = ['Name', 'slug']


admin.site.register(bproposals, ProposalBuildAdmin)