from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = u'Профиль'
    verbose_name_plural = u'Профиль'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name = u'Профиль'
#     verbose_name_plural = u'Профиль'
#     fk_name = 'user'
#
#
# # @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )
#     list_display = ('username', 'last_name', 'first_name', 'is_active',
#                     'get_phone', 'get_birthday', 'get_groups', 'get_location')
#     list_filter = ('is_active', 'groups')
#     search_fields = ('username', 'first_name', 'last_name')
#
#     list_select_related = True
#
#     def get_groups(self, instance):
#         list_groups = ''
#         for group in instance.groups.all():
#             if list_groups == '':
#                 list_groups = group.name
#             else:
#                 list_groups = list_groups + ', ' + group.name
#         return list_groups
#     get_groups.short_description = u'Группы'
#
#     def get_location(self, instance):
#         return instance.profile.location
#     get_location.short_description = u'Город'
#
#     def get_birthday(self, instance):
#         return instance.profile.birthday
#     get_birthday.short_description = u'Дата рождения'
#
#     def get_phone(self, instance):
#         return instance.profile.phone
#     get_phone.short_description = u'Номер'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)