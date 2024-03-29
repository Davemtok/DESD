from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
#     # Endpoint for querying all tasks
#     # This is a GET request
#     path("tasks/", views.tasks, name="tasks"),
    
#     # Endpoint for creating a new task
#     # This is a POST request
#     path("create/", views.create_task, name="create_task"),
    
#     # Endpoint for updating a task
#     # This is a POST request
#     path("update/<int:pk>/", views.update_task,
#          name="update_task"),
    
#     # Endpoint for deleting a task
#     # This is a POST request
#     path("remove/<int:pk>/", views.delete_task,
#          name="delete_task"),
    
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('booking', views.booking, name='booking'),
    path('bookingSuccess', views.bookingSuccess, name='bookingSuccess'),
    path('bookingCancel', views.bookingCancel, name='bookingCancel'),
    path('bookings/current_day/', views.BookingScheduelView, name='bookings_for_current_day'),
    path('cancel-booking/<str:date>/<str:time>/', views.bookingCancelMethod, name='bookingCancelMethod'),

]
