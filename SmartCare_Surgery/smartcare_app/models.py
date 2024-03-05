from django.db import models


class Task(models.Model):
    """
    Task model
    Database table name: task_management_task
    """

    # Task title
    title = models.CharField(max_length=100)
    # Task description
    description = models.TextField()
    # Task status (completed or not)
    completed = models.BooleanField(default=False)
    # Task creation date
    created_at = models.DateTimeField(auto_now_add=True)
