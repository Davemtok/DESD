from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def doctor_dashboard(request):
    # Ensure the user is a doctor
    
    context = {
        # 'doctor_info': doctor_info,
    }
    
    return render(request, 'doctors/dashboard.html', context)
