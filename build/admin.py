from django.contrib import admin

# Register your models here.
from build.models import acts_build, build_request, TypeRequest_build

class ActsBuildInline(admin.StackedInline):
    model = acts_build
    extra = 1

class RequestBuildAdmin(admin.ModelAdmin):
    list_display = ['Client','AddressObject','TypeRequest','Company','Status']
    inlines = [ActsBuildInline]

class TypeRequestBuildAdmin(admin.ModelAdmin):
    list_display = ['Name','slug']

admin.site.register(build_request, RequestBuildAdmin)
admin.site.register(TypeRequest_build, TypeRequestBuildAdmin)