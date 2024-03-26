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
    
    path('', views.Home, name='Home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('contact/', views.Contact, name='contact'),
    path('about/', views.About, name='about'),
]
