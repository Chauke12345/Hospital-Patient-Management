from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, Patient, Doctor


@login_required(login_url='login')
def appointments(request):

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        date = request.POST.get("date")
        time = request.POST.get("time")
        reason = request.POST.get("reason")

        # VALIDATION
        if not patient_id or not doctor_id:
            return render(request, "hospital/appointments.html", {
                "patients": patients,
                "doctors": doctors,
                "error": "Patient and Doctor are required"
            })

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            reason=reason
        )

        return redirect("appointments")

    return render(request, "hospital/appointments.html", {
        "patients": patients,
        "doctors": doctors
    })