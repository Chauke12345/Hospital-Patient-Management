from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    gender = models.CharField(max_length=50, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, blank=True, null=True)

    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date}"


# =========================
# PRESCRIPTION (HERE IT IS)
# =========================
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    medication = models.TextField()
    dosage = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"