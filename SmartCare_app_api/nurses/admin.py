# Register your models here.
from django.contrib import admin
from .models import Nurse

class NurseAdmin(admin.ModelAdmin):
    list_display = ['user'] # Adjust as necessary
    search_fields = ['user__username', 'user__first_name', 'user__last_name'] # Enable search functionality

admin.site.register(Nurse, NurseAdmin)
