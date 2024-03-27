from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import User

@login_required
def patient_dashboard(request):
    if request.user.is_patient:
        # Logic to fetch patient-specific information can go here
        return render(request, 'patients/dashboard.html')
    else:
        return redirect('home')  # Or some 'access denied' page
