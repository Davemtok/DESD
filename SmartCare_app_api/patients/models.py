from django.db import models

# Create your models here.
from django.db import models
from core.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Additional fields for patients
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from appointments.models import Prescription

class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'prescriptions/patient_prescriptions.html'

    def get_queryset(self):
        """Override to return only the prescriptions for the logged-in patient."""
        return Prescription.objects.filter(patient__user=self.request.user)