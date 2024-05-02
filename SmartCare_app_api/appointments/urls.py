from django import views
from django.urls import path
from .views import book_appointment, appointment_list, edit_appointment, issue_prescription, view_prescriptions
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

]

