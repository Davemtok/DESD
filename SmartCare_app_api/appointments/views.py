from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
import datetime
from datetime import datetime, timedelta

from .models import Appointment, Prescription
from .forms import AppointmentBookingForm, AppointmentEditForm, PrescriptionForm
from django.urls import reverse
from django.utils import timezone


def calculate_available_slots(events, start_of_day, end_of_day, appointment_duration=30):
    available_slots = []
    current_time = start_of_day

    for event in events:
        event_start = datetime.fromisoformat(event['start'].get('dateTime'))
        if current_time < event_start:
            while current_time + timedelta(minutes=appointment_duration) <= event_start:
                available_slots.append(current_time.strftime('%H:%M'))
                current_time += timedelta(minutes=appointment_duration)
        event_end = datetime.fromisoformat(event['end'].get('dateTime'))
        current_time = max(current_time, event_end)
    
    # Check for slots after the last event until the end of business hours
    while current_time + timedelta(minutes=appointment_duration) <= end_of_day:
        available_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=appointment_duration)
    
    return available_slots

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentBookingForm

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Your appointment has been booked.')
            return redirect("appointments:appointment_list")  # Adjust to your named URL for the appointments list
    else:
        form = AppointmentBookingForm()
    return render(request, 'book_appointment.html', {'form': form})


from django.shortcuts import render
from .models import Appointment

@login_required
def appointment_list(request):
    if request.user.is_doctor or request.user.is_nurse:
        # Doctors see appointments where they are the provider
        appointments = Appointment.objects.filter(provider=request.user).order_by('appointment_date', 'appointment_time')
    else:
        # Logic for patients or other roles
        appointments = Appointment.objects.none()  # or another appropriate queryset

    return render(request, 'appointment_list.html', {'appointments': appointments})

# In your appointments/views.py
from django.http import HttpResponseRedirect
from .forms import AppointmentEditForm

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, provider=request.user)  # Ensure only the doctor can edit their appointments
    if request.method == 'POST':
        form = AppointmentEditForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('appointments:appointment_list'))
    else:
        form = AppointmentEditForm(instance=appointment)
    
    return render(request, 'edit_appointment.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment

@login_required
def appointment_list(request):
    if request.user.is_doctor:  # Ensure your User model has an 'is_doctor' attribute or adjust accordingly
        appointments = Appointment.objects.filter(provider=request.user).order_by('appointment_date', 'appointment_time')
    else:
        appointments = Appointment.objects.filter(patient=request.user).order_by('appointment_date', 'appointment_time')

    return render(request, 'appointment_list.html', {'appointments': appointments})


@login_required
def issue_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.prescribed_by = request.user
            prescription.prescribed_to = appointment.patient
            prescription.save()
            messages.success(request, "Prescription issued successfully.")
            return redirect('appointments:appointment_detail', appointment_id=appointment.id)
    else:
        form = PrescriptionForm()
    return render(request, 'issue_prescription.html', {'form': form, 'appointment': appointment})

from django.shortcuts import get_object_or_404, render
from .models import Appointment

from django.shortcuts import render, get_object_or_404
from .models import Appointment

def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    # Assuming `prescriptions` is the related_name for the Prescription model
    prescriptions = appointment.prescriptions.all()
    return render(request, 'appointment_detail.html', {
        'appointment': appointment,
        'prescriptions': prescriptions,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment, Prescription

@login_required
def my_health_overview(request):
    # Fetch appointments and prescriptions for the logged-in user
    appointments = Appointment.objects.filter(patient__user=request.user)
    prescriptions = Prescription.objects.filter(patient__user=request.user)
    
    # Pass both to the template
    return render(request, 'my_health_overview.html', {
        'appointments': appointments,
        'prescriptions': prescriptions
    })


@login_required
def view_prescriptions(request):
    # Fetch all appointments where the current user is the patient
    appointments = Appointment.objects.filter(patient=request.user)
    
    # Fetch all prescriptions related to those appointments
    prescriptions = Prescription.objects.filter(appointment__in=appointments).order_by('-date_issued')  # Assuming there's a 'date_issued' field in Prescription
    
    return render(request, 'prescriptions_list.html', {'prescriptions': prescriptions})


from django.utils import timezone
from django.shortcuts import render
from .models import Appointment

@login_required
def daily_surgery_schedule(request):
    if not request.user.is_doctor:
        return render(request, 'error.html', {'message': 'Unauthorized access.'})

    # Handle POST request for updates or cancellations
    if request.method == 'POST':
        if 'edit_surgery' in request.POST:
            form = AppointmentBookingForm(request.POST, instance=get_object_or_404(Appointment, pk=request.POST.get('surgery_id'), is_surgery=True))
            if form.is_valid():
                form.save()
        elif 'cancel_surgery' in request.POST:
            surgery = get_object_or_404(Appointment, pk=request.POST.get('surgery_id'), is_surgery=True)
            surgery.status = 'cancelled'
            surgery.save()

    # Regardless of POST or GET, load surgeries
    surgeries = Appointment.objects.filter(provider=request.user, is_surgery=True).order_by('appointment_date', 'appointment_time')
    return render(request, 'doctor_surgery_schedule.html', {'surgeries': surgeries})

from django.shortcuts import redirect, get_object_or_404
from .models import Appointment

def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    # Ensure that the user has permission to cancel the appointment
    if request.user == appointment.patient or request.user == appointment.provider:
        appointment.status = 'cancelled'
        appointment.save()
        # Redirect to an appropriate page
        return redirect('appointments:appointment_list')
    else:
        # Return an error message or redirect to a forbidden access page
        return redirect('error_page')
    
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentBookingForm  # Ensure this form is created in forms.py

@login_required
def edit_surgery(request, id):
    surgery = get_object_or_404(Appointment, pk=id, is_surgery=True)
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, instance=surgery)
        if form.is_valid():
            form.save()
            return redirect('appointments:daily_surgery_schedule')  # Adjust the redirect as necessary
    else:
        form = AppointmentBookingForm(instance=surgery)
    return render(request, 'edit_surgery.html', {'form': form})

@login_required
def cancel_surgery(request, id):
    surgery = get_object_or_404(Appointment, pk=id, is_surgery=True)
    if request.method == 'POST':
        surgery.status = 'cancelled'
        surgery.save()
        return redirect('appointments:daily_surgery_schedule')
    return render(request, 'confirm_cancel_surgery.html', {'surgery': surgery})
