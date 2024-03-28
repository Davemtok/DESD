from django.urls import path
from .views import book_appointment
from .views import appointment_list
from .views import edit_appointment



app_name = 'appointments'

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    # Include other URLs for your app
    path('list/', appointment_list, name='appointment_list'),
    path('edit/<int:appointment_id>/', edit_appointment, name='edit_appointment'),


]

