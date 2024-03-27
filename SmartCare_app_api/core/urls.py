from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Home page at the root URL
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),  # Assuming you have a logout view
    # Include the dashboard URLs from the doctors, nurses, and patients apps
    path('doctors/', include('doctors.urls')),
    path('nurses/', include('nurses.urls')),
    path('patients/', include('patients.urls')),
]
