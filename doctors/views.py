from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from appointments.models import Appointment
from pharmacy.models import Prescription
from pharmacy.forms import PrescriptionForm

from doctors.models import Doctor
from patients.models import Patient


# =========================
# DOCTOR DASHBOARD
# =========================
@login_required
def doctor_dashboard(request):

    # If doctor is logged in via User system, you must link properly later
    appointments = Appointment.objects.filter()

    return render(request, 'doctor/dashboard.html', {
        'appointments': appointments
    })


# =========================
# APPOINTMENT DETAIL
# =========================
@login_required
def appointment_detail(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'doctor/appointment_detail.html', {
        'appointment': appointment
    })


# =========================
# CREATE PRESCRIPTION
# =========================
@login_required
def create_prescription(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    form = PrescriptionForm()

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = form.save(commit=False)

            prescription.patient = patient
            prescription.doctor = None  # FIX LATER (or link doctor properly)

            prescription.save()

            return redirect('doctor_dashboard')

    return render(request, 'doctor/create_prescription.html', {
        'form': form,
        'patient': patient
    })


# =========================
# DOCTOR LIST (FIXED)
# =========================
def doctor_list(request):

    doctors = Doctor.objects.all()

    return render(request, "doctors/doctor_list.html", {
        "doctors": doctors
    })