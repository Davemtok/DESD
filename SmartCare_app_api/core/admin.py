from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved', 'is_active', 'is_doctor', 'is_nurse', 'is_patient')
    list_filter = ('is_approved', 'is_active', 'is_doctor', 'is_nurse', 'is_patient')
    search_fields = ('username', 'email')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)
    approve_users.short_description = 'Approve selected users'

# Register the custom User model with the customized admin interface
admin.site.register(User, UserAdmin)