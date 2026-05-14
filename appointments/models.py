from django.db import models


# =========================
# APPOINTMENT MODEL
# Links patients and doctors for scheduled visits
# =========================
class Appointment(models.Model):

    # Link to Patient model (from patients app)
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE
    )

    # Link to Doctor model (from doctors app)
    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.CASCADE
    )

    # Appointment scheduling details
    date = models.DateField()
    time = models.TimeField()

    # Optional reason for visit
    reason = models.TextField(blank=True, null=True)

    # Auto-generated timestamp when appointment is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Human-readable display in admin panel
        return f"{self.patient} → {self.doctor} ({self.date})"