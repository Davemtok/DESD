from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserCreationForm(UserCreationForm):
    is_nurse = forms.BooleanField(required=False)
    is_doctor = forms.BooleanField(required=False)
    is_patient = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_nurse', 'is_doctor', 'is_patient', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_nurse = self.cleaned_data['is_nurse']
        user.is_doctor = self.cleaned_data['is_doctor']
        user.is_patient = self.cleaned_data['is_patient']
        user.is_staff = self.cleaned_data['is_staff']
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    postcode = forms.CharField(required=True)
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    is_private_client = forms.BooleanField(initial=True, required=False)  # Default to private client

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'address', 'postcode', 'dob', 'is_private_client')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.postcode = self.cleaned_data['postcode']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        
# forms.py
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User

class CustomUserChangeForm(UserChangeForm):
    is_approved = forms.BooleanField(required=False)  # Add this if it's not part of the default User model
    is_superuser = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    
    class Meta:
        model = User
        fields = ('is_active', 'is_approved', 'is_superuser', 'is_staff', 'is_doctor', 'is_nurse', 'is_patient')


