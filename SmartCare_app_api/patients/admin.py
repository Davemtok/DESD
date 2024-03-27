from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user'] # Adjust as necessary
    search_fields = ['user__username', 'user__first_name', 'user__last_name'] # Enable search functionality

admin.site.register(Patient, PatientAdmin)
