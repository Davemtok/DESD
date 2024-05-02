from django.urls import path
from .views import daily_surgery_schedule, doctor_dashboard

urlpatterns = [
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor/surgery-schedule/', daily_surgery_schedule, name='daily_surgery_schedule'),

]
