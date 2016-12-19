from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.dao.models import *
from apps.accounts.models import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'birthdate', 'adress')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Employee)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Invoice)
