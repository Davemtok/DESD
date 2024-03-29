from django.db import models
from django.contrib.auth.models import User


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


class Booking(models.Model):
    subject = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    comments = models.TextField(blank=True)
    doctor = models.CharField(max_length=100)

    def __str__(self):
        return self.subject