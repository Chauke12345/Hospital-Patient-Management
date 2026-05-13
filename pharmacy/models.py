from django.db import models
from patients.models import Patient
from accounts.models import User

class Prescription(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('DISPENSED', 'Dispensed'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'DOCTOR'}
    )

    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    instructions = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.medicine_name}"