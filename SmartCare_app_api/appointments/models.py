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

