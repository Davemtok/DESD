# Create your views here.
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import path
from . import views
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# def home(request):
#     return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB just yet
            user.is_active = False  # Deactivate account until admin approves
            user.is_approved = False  # Mark as not approved
            user.save()  # Now save the user to DB
            # Redirect to login page after successful registration
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_approved:  # Check if user is approved
                login(request, user)
                # Redirect based on the user type
                if user.is_doctor:
                    return redirect('doctors:doctor_dashboard')
                elif user.is_nurse:
                    return redirect('nurses:nurse_dashboard')
                elif user.is_patient:
                    return redirect('patients:patient_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Account is not approved by admin yet.')  # Inform user if not approved
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})



from django.shortcuts import redirect, render
from django.contrib.auth import logout
def user_logout(request):
    logout(request)  # This will log out the current user
    return redirect('user_login')  # Redirect to login page or home page after logout

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def doctor_dashboard(request):
    # Add logic specific to doctor users here
    return render(request, 'doctors:doctor_dashboard')

@login_required
def nurse_dashboard(request):
    # Add logic specific to nurse users here
    return render(request, 'nurses:nurse_dashboard')

@login_required
def patient_dashboard(request):
    # Add logic specific to patient users here
    return render(request, 'patients:patient_dashboard')
