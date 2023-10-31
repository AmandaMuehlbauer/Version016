# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


#class UserAdmin(BaseUserAdmin):
 #   list_display = ('email', 'username', 'is_active', 'is_staff',)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username',)}),  # Exclude 'first_name' and 'last_name'
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),  # Exclude 'date_joined'
    )
    list_display = ('email', 'username', 'is_active', 'is_staff')


admin.site.register(User, UserAdmin)
