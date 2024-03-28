from django import forms
from core.models import User  # Make sure to import your custom User model
from .models import Appointment

class AppointmentBookingForm(forms.ModelForm):
    provider = forms.ModelChoiceField(queryset=User.objects.filter(is_doctor=True), required=True, label="Doctor")
    appointment_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['provider', 'appointment_date', 'appointment_time']
        
class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'status']  # Customize as needed

