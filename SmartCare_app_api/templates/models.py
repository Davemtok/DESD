# models.py
from django.db import models

class Patient(models.Model):
    gender = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)

class Bed(models.Model):
    date = models.DateField()
    total_beds = models.IntegerField()
    occupied_beds = models.IntegerField()

# Define other models similarly for appointment, staffing, financial, quality, emergency, operational, and clinical data
