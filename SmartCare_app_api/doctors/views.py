from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment

@login_required
def doctor_dashboard(request):
    if hasattr(request.user, 'is_doctor') and request.user.is_doctor:
        appointments = Appointment.objects.filter(provider=request.user).order_by('appointment_date', 'appointment_time')
        return render(request, 'doctors/dashboard.html', {'appointments': appointments})
    else:
        # Redirect or show an error if the user is not a doctor
        return redirect('home')  # adjust the redirection as needed