from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user'] # with the actual field names
    search_fields = ['user__username', 'user__first_name', 'user__last_name'] # Enable search by user's username, first name, and last name

admin.site.register(Doctor, DoctorAdmin)
