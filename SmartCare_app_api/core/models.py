# core/models.py

from django.utils import timezone  # Corrected import
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True)
    dob = models.DateField(default=timezone.now)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=12, blank=True, null=True)
    is_private_client = models.BooleanField(default=False)

