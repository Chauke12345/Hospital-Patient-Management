from django.db import models



from django.db import models
from doctors.models import Doctor


class Patient(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=100)

    age = models.IntegerField(null=True, blank=True)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    ward = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    reason = models.TextField(
        null=True,
        blank=True
    )

    priority = models.CharField(
        max_length=100,
        default="Normal"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_inpatient = models.BooleanField(default=False)

    admitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# PRESCRIPTION MODEL
# Medical prescriptions issued by doctors
# =========================
class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    medication = models.TextField()

    dosage = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"