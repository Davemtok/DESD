from django.db import models

# Create your models here.
from django.db import models
from core.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Additional fields for patients
