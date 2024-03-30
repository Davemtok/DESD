from django.db import models
from django.conf import settings

# Assuming you have a User model in your Django project
# which could be the default auth user model or a custom user model
# Adjust the User model import according to your project structure

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    # Linking to the Django user model, adjust based on your user model setup
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments_as_patient', on_delete=models.CASCADE)
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments_as_provider', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    # You can add more fields as needed, for instance, a field for notes or appointment type

    def __str__(self):
        return f"{self.patient}'s appointment with {self.provider} on {self.appointment_date} at {self.appointment_time}"

class Prescription(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescribed_prescriptions')
    prescribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_prescriptions')
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField()
    date_issued = models.DateField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.medication} to {self.prescribed_to.username} by {self.prescribed_by.username}"




