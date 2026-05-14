from django.db import models


# =========================
# DOCTOR MODEL
# Stores doctor details
# =========================
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)

    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        # Display format in admin and dropdowns
        return f"Dr. {self.first_name} {self.last_name}"


# =========================
# PATIENT MODEL
# Stores patient details + assigned doctor
# =========================
class Patient(models.Model):
    name = models.CharField(max_length=100)

    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    gender = models.CharField(max_length=50, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    

    reason = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, blank=True, null=True)

    # Optional assigned doctor (can be null)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# =========================
# APPOINTMENT MODEL
# Links patient + doctor with date/time
# =========================
class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    date = models.DateField()
    time = models.TimeField()

    reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → {self.doctor} ({self.date})"


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