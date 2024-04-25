# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Patient, Bed

def dashboard(request):
    return render(request, 'dashboard.html')

def get_data(request):
    patient_data = list(Patient.objects.values())
    bed_data = list(Bed.objects.values())
    # Fetch other data similarly for appointment, staffing, financial, quality, emergency, operational, and clinical data
    return JsonResponse({
        'patient_data': patient_data,
        'bed_data': bed_data,
        # Pass other data to the frontend similarly
    })
