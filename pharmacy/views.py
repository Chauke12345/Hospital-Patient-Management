from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Prescription

@login_required
def pharmacy_dashboard(request):
    prescriptions = Prescription.objects.all()

    return render(request, 'pharmacy/dashboard.html', {
        'prescriptions': prescriptions
    })