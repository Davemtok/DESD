from django.urls import path
from .views import nurse_dashboard

urlpatterns = [
    path('dashboard/', nurse_dashboard, name='nurse_dashboard'),
]
