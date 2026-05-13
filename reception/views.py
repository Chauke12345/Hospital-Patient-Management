from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from patients.models import Patient
from doctors.models import Doctor   # IMPORTANT


# =========================
# RECEPTION DASHBOARD
# =========================
@login_required(login_url='login')
def reception_dashboard(request):

    inpatients = Patient.objects.filter(is_inpatient=True)

    return render(request, 'reception/dashboard.html', {
        'inpatients': inpatients,
        'total_inpatients': inpatients.count(),
    })


# =========================
# ADMIT PATIENT
# =========================
@login_required(login_url='login')
def admit_patient(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    patient.is_inpatient = True
    patient.admitted_at = timezone.now()
    patient.save()

    return redirect('reception_dashboard')


# =========================
# ADD NEW PATIENT (FORM)
# =========================
from .forms import PatientForm


@login_required(login_url='login')
def add_patient(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('reception_dashboard')

    else:
        form = PatientForm()

    return render(request, 'reception/add_patient.html', {
        'form': form
    })


# =========================
# RECEPTION ADMISSION FORM (MANUAL)
# =========================
@login_required(login_url='login')
def reception(request):

    doctors = Doctor.objects.all()
    error = None

    if request.method == 'POST':

        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        ward = request.POST.get('ward')
        reason = request.POST.get('reason')
        priority = request.POST.get('priority')
        doctor_id = request.POST.get('doctor')

        if not name or not age or not doctor_id:
            return render(request, 'hospital/reception.html', {
                'doctors': doctors,
                'error': "Name, Age and Doctor are required"
            })

        doctor = get_object_or_404(Doctor, id=doctor_id)

        Patient.objects.create(
            name=name,
            age=age,
            gender=gender,
            phone=phone,
            ward=ward,
            reason=reason,
            priority=priority,
            doctor=doctor
        )

        return redirect('patients')

    return render(request, 'hospital/reception.html', {
        'doctors': doctors
    })