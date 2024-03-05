from django.urls import path
from . import views


urlpatterns = [
    # Endpoint for querying all tasks
    # This is a GET request
    path("tasks/", views.tasks, name="tasks"),
    # Endpoint for creating a new task
    # This is a POST request
    path("create/", views.create_task, name="create_task"),
    # Endpoint for updating a task
    # This is a POST request
    path("update/<int:pk>/", views.update_task,
         name="update_task"),
    # Endpoint for deleting a task
    # This is a POST request
    path("remove/<int:pk>/", views.delete_task,
         name="delete_task"),
]
