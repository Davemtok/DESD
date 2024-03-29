from django import forms
from datetime import datetime, date

class BookingForm(forms.Form):
    subject = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    comment = forms.CharField(widget=forms.Textarea)
