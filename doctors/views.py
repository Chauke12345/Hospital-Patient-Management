from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment

@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user)

    return render(request, 'doctor/dashboard.html', {
        'appointments': appointments
    })

from patients.models import Patient

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'doctor/appointment_detail.html', {
        'appointment': appointment
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pharmacy.models import Prescription
from pharmacy.forms import PrescriptionForm

@login_required
def create_prescription(request, patient_id):
    form = PrescriptionForm()

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            return redirect('doctor_dashboard')

    return render(request, 'doctor/create_prescription.html', {'form': form})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors/doctor_list.html", {"doctors": doctors})