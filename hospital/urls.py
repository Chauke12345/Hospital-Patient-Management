from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # keep ONLY ONE homepage

    path('reception/', views.reception, name='reception'),
    path('appointments/', views.appointments, name='appointments'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('patients/', views.patient_list, name='patients'),
]