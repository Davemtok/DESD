from django.urls import path
from .views import patient_dashboard, view_prescriptions
from .models import PrescriptionListView

urlpatterns = [
    path('dashboard/', patient_dashboard, name='patient_dashboard'),
    path('my-prescriptions/', PrescriptionListView.as_view(), name='my-prescriptions'),
    path('prescriptions/', view_prescriptions, name='view_prescriptions'),

]
