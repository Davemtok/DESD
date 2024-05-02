from django import forms
from core.models import User  # Make sure to import your custom User model
from .models import Appointment

from django import forms
from django.db import models  # This import is necessary for models.Q
from django.contrib.auth import get_user_model

User = get_user_model()

User = get_user_model()

class AppointmentBookingForm(forms.ModelForm):
    provider = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Initially empty, set in __init__
        label="Provider",
        help_text="Select a doctor or a nurse for the appointment."
    )
    appointment_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    appointment_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any specific issues or requests?'}), required=False)
    is_surgery = forms.BooleanField(required=False, help_text="Check if this is a surgical appointment")

    class Meta:
        model = Appointment
        fields = ['provider', 'appointment_date', 'appointment_time', 'description', 'is_surgery']

    def __init__(self, *args, **kwargs):
        super(AppointmentBookingForm, self).__init__(*args, **kwargs)
        # Set the provider queryset to include only doctors and nurses
        self.fields['provider'].queryset = User.objects.filter(
            models.Q(is_doctor=True) | models.Q(is_nurse=True)
        )


        
class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'status']  # Customize as needed

from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'instructions', 'cost']