from django.urls import path
from .views import patient_dashboard

urlpatterns = [
    path('dashboard/', patient_dashboard, name='patient_dashboard'),
]
