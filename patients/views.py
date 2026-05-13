from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm
from django.contrib.auth.decorators import login_required

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


@login_required
def add_patient(request):
    form = PatientForm()

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')

    return render(request, 'patients/add_patient.html', {'form': form})