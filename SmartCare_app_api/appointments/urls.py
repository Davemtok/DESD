from django import views
from django.urls import path
from .views import book_appointment, appointment_list, cancel_surgery, daily_surgery_schedule, edit_appointment, edit_surgery, issue_prescription, view_prescriptions
from . import views
from .views import my_health_overview


app_name = 'appointments'

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('list/', appointment_list, name='appointment_list'),
    path('edit/<int:appointment_id>/', edit_appointment, name='edit_appointment'),
    path('<int:appointment_id>/issue_prescription/', issue_prescription, name='issue_prescription'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('my-health-overview/', my_health_overview, name='my-health-overview'),
    path('prescriptions/', view_prescriptions, name='view_prescriptions'),
    path('doctor/surgery-schedule/', daily_surgery_schedule, name='daily_surgery_schedule'),
    path('cancel_appointment/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
    path('edit_surgery/<int:id>/', edit_surgery, name='edit_surgery'),
    path('cancel_surgery/<int:id>/', cancel_surgery, name='cancel_surgery'),
]

