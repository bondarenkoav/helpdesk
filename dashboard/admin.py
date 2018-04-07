from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from claim.models import CategoryMenu

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

admin.site.register(CategoryMenu, DraggableMPTTAdmin)
