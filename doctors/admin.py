from django.contrib import admin
from .models import Doctor


# =========================
# DOCTOR ADMIN CONFIGURATION
# Controls how Doctor model appears in Django admin panel
# =========================
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    # Columns shown in admin list view
    list_display = (
        "first_name",
        "last_name",
        "specialization",
        "phone",
        "email"
    )

    # Enables search bar in admin
    search_fields = (
        "first_name",
        "last_name",
        "specialization"
    )