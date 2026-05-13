from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('prescription/<int:patient_id>/', views.create_prescription, name='create_prescription'),
]