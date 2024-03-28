from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
import datetime
from datetime import datetime, timedelta

from django.urls import reverse


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

from django.shortcuts import render, redirect
from .forms import AppointmentBookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = 'scheduled'  # Assuming 'scheduled' is a valid status
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
    if request.user.is_doctor:
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
