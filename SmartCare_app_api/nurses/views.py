from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import User

@login_required
def nurse_dashboard(request):
    if request.user.is_nurse:
        # Logic to fetch nurse-specific information can go here
        return render(request, 'nurses/dashboard.html')
    else:
        return redirect('home')  # Or some 'access denied' page
