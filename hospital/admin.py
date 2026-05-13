# Import the Django admin module
from django.contrib import admin

# Import your models from the current app
from .models import (
    Doctor,
    Patient,
    Appointment,
    Prescription
)

# Register models with the Django admin site
# This makes them accessible via the Django admin interface

# Register Doctor model so admins can manage doctors in the admin panel
admin.site.register(Doctor)

# Register Patient model so admins can manage patients in the admin panel
admin.site.register(Patient)

# Register Appointment model so admins can manage appointments in the admin panel
admin.site.register(Appointment)

# Register Prescription model so admins can manage prescriptions in the admin panel
admin.site.register(Prescription)