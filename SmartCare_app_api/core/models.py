# core/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
