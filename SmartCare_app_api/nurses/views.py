from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment


@login_required
def nurse_dashboard(request):
    if request.user.is_nurse:  # Ensure your User model has an 'is_nurse' attribute or similar
        appointments = Appointment.objects.filter(provider=request.user).order_by('appointment_date', 'appointment_time')
        return render(request, 'nurses/dashboard.html', {'appointments': appointments})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})
