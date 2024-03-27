from django.db import models

# Create your models here.
from django.db import models
from core.models import User

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Additional fields for nurses
