from django.db import models
from doctors.models import Doctor


class Patient(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=200)

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="Other"
    )

    phone = models.CharField(
        max_length=100,
        blank=True,
        default=""
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
        max_length=50,
        default="Normal"
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )

    is_inpatient = models.BooleanField(default=False)

    admitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name