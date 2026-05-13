from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('reception/', views.reception, name='reception'),

    path('patients/', views.patients, name='patients'),

    path('appointments/', views.appointments, name='appointments'),

    path('logout/', views.logout_view, name='logout'),

    path('prescriptions/', views.prescriptions, name='prescriptions'),
]