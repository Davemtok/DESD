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


def home(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB just yet
            user.is_active = False  # Deactivate account until admin approves
            user.is_approved = False  # Mark as not approved
            user.postcode = form.cleaned_data.get('postcode')  # Ensure postcode is saved
            user.address = form.cleaned_data.get('address')  # Ensure location is saved
            user.save()  # Now save the user to DB
            # Redirect to login page after successful registration
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

from django.contrib.auth.models import Group

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_approved:  # Check if user is approved
                login(request, user)
                # Check if the user is an admin
                if user.is_superuser or (user.groups.filter(name='Admins').exists()):
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
                elif user.is_doctor:
                    return redirect('doctors:doctor_dashboard')
                elif user.is_nurse:
                    return redirect('nurses:nurse_dashboard')
                elif user.is_patient:
                    return redirect('patients:patient_dashboard')
                else:
                    return redirect('home')  # Redirect to a generic home page if no role is matched
            else:
                messages.error(request, 'Account is not approved by admin yet.')  # Inform user if not approved
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})



from django.shortcuts import redirect, render
from django.contrib.auth import logout
def user_logout(request):
    logout(request)  # This will log out the current user
    return redirect('home')  # Redirect to login page or home page after logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

@login_required
def admin_dashboard(request):
    User = get_user_model()
    users = User.objects.all().order_by('username')  # List users ordered by username

    if request.method == 'POST':
        # Handle updates from form submissions
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        # Update user properties based on checkboxes
        user.is_approved = 'is_approved' in request.POST
        user.is_superuser = 'is_superuser' in request.POST
        user.is_staff = 'is_staff' in request.POST
        user.is_active = 'is_active' in request.POST
        user.is_doctor = 'is_doctor' in request.POST
        user.is_nurse = 'is_nurse' in request.POST
        user.is_patient = 'is_patient' in request.POST
        user.is_private_client = 'is_patient' in request.POST

        # Save the updated user information
        user.save()
        messages.success(request, f"Updated {user.username}'s profile successfully.")
        return redirect('admin_dashboard')

    # Render the admin dashboard page with the user list
    return render(request, 'admin_dashboard.html', {'users': users})


