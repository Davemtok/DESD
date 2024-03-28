"""smartcare_app_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import home  # Import the home view from core app
from appointments.views import book_appointment,appointment_list  # Import the home view from core app



urlpatterns = [
    path('', home, name='home'),  # Home page at the root URL
    path('book/', book_appointment, name='book_appointment'),
    path('list/', appointment_list, name='appointment_list'),
    path('appointments/', include('appointments.urls', namespace='appointments')),  # Include the appointments URLs
    path('admin/', admin.site.urls),
    path('doctors/', include(('doctors.urls', 'doctors'), namespace='doctors')),
    path('nurses/', include(('nurses.urls','nurses'), namespace='nurses')),
    path('patients/', include(('patients.urls','patients'), namespace='patients')),
    path("core/", include("core.urls")),
]
