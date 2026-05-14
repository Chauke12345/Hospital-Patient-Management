from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('reception/', views.reception, name='reception'),

    path('patients/', views.patients, name='patients'),

    path('appointments/', views.appointments, name='appointments'),

    path('prescriptions/', views.prescriptions, name='prescriptions'),
]