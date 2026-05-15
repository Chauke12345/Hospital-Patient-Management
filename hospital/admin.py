from django.contrib import admin
from .models import Patient, Prescription

admin.site.register(Patient)
admin.site.register(Prescription)