from django.urls import path
from . import views

urlpatterns = [
    path('', views.pharmacy_dashboard, name='pharmacy_dashboard'),
]