from django.shortcuts import render, redirect

from .models import Patient, Doctor, Appointment, Prescription


# -----------------------------
# DASHBOARD (NO LOGIN REQUIRED)
# -----------------------------
def dashboard(request):
    return render(request, "hospital/dashboard.html", {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "total_prescriptions": Prescription.objects.count(),
    })


# -----------------------------
# PATIENT LIST
# -----------------------------
def patients(request):
    return render(request, "hospital/patients.html", {
        "patients": Patient.objects.all().order_by('-id')
    })


# -----------------------------
# RECEPTION
# -----------------------------
def reception(request):
    doctors = Doctor.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")

        if not doctor_id:
            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": "Please select a doctor"
            })

        doctor = Doctor.objects.get(id=doctor_id)

        Patient.objects.create(
            name=request.POST.get("name") or "Unknown",
            age=request.POST.get("age") or 0,
            gender=request.POST.get("gender") or "Not specified",
            phone=request.POST.get("phone") or "N/A",
            ward=request.POST.get("ward") or "General",
            reason=request.POST.get("reason") or "",
            priority=request.POST.get("priority") or "Normal",
            doctor=doctor
        )

        return redirect("patients")

    return render(request, "hospital/reception.html", {
        "doctors": doctors
    })


# -----------------------------
# APPOINTMENTS
# -----------------------------
def appointments(request):

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")

        if not doctor_id or not patient_id:
            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": Appointment.objects.all(),
                "error": "Please select doctor and patient"
            })

        Appointment.objects.create(
            doctor_id=doctor_id,
            patient_id=patient_id,
            date=request.POST.get("date"),
            time=request.POST.get("time"),
            reason=request.POST.get("reason", "")
        )

        return redirect("appointments")

    return render(request, "hospital/appointments.html", {
        "doctors": doctors,
        "patients": patients,
        "appointments": Appointment.objects.all()
    })


# -----------------------------
# PRESCRIPTIONS
# -----------------------------
def prescriptions(request):

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        Prescription.objects.create(
            patient=patient,
            doctor=doctor,
            medication=request.POST.get("medication"),
            dosage=request.POST.get("dosage"),
            instructions=request.POST.get("instructions"),
        )

        return redirect("prescriptions")

    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": Prescription.objects.all().order_by("-id")
    })