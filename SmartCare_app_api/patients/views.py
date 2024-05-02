from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import User
from appointments.models import Appointment, Prescription

@login_required
def patient_dashboard(request):
    if request.user.is_patient:
        print("User is a patient")
        # Fetch appointments where the current user is the patient
        appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date', '-appointment_time')
        # Pass the appointments to the template
        return render(request, 'patients/dashboard.html', {'appointments': appointments})
    else:
        return redirect('home')  # Or some 'access denied' page
    
@login_required
def view_prescriptions(request):
    # Fetch all appointments where the current user is the patient
    appointments = Appointment.objects.filter(patient=request.user)
    
    # Fetch all prescriptions related to those appointments
    prescriptions = Prescription.objects.filter(appointment__in=appointments).order_by('-date_issued')  # Assuming there's a 'date_issued' field in Prescription
    
    return render(request, 'prescriptions_list.html', {'prescriptions': prescriptions})


