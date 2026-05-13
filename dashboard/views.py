from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from patients.models import Patient
from accounts.models import User
from appointments.models import Appointment
from pharmacy.models import Prescription


@login_required
def admin_dashboard(request):

    patients_count = Patient.objects.count()
    doctors_count = User.objects.filter(role='DOCTOR').count()
    appointments_count = Appointment.objects.count()
    prescriptions_count = Prescription.objects.count()

    return render(request, 'admin/dashboard.html', {
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'appointments_count': appointments_count,
        'prescriptions_count': prescriptions_count,
    })