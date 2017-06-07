from django.contrib import admin
from sim.models import UseTypeSIM


class UseTypeSIMAdmin(admin.ModelAdmin):
    list_display = ['Name','slug']

admin.site.register(UseTypeSIM, UseTypeSIMAdmin)
