from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone

from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from hospital.models import Prescription   # keep ONLY if correct

User = get_user_model()


# ==========================================
# LOGIN VIEW
# ==========================================
def login_view(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "Please enter username and password"

        else:
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)
                return redirect("dashboard")

            error = "Invalid username or password"

    return render(request, "hospital/login.html", {
        "error": error
    })


# ==========================================
# LOGOUT VIEW
# ==========================================
@login_required(login_url='login')
def logout_view(request):

    logout(request)

    return redirect("login")


# ==========================================
# DASHBOARD VIEW
# ==========================================
@login_required(login_url='login')
def dashboard(request):

    context = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "total_prescriptions": Prescription.objects.count(),
    }

    return render(request, "hospital/dashboard.html", context)


# ==========================================
# PATIENT LIST VIEW
# ==========================================
@login_required(login_url='login')
def patient_list(request):

    patients = Patient.objects.all().order_by("-id")

    return render(request, "hospital/patients.html", {
        "patients": patients
    })


# ==========================================
# RECEPTION / REGISTER PATIENT
# ==========================================
@login_required(login_url='login')
def reception(request):

    doctors = Doctor.objects.all()

    if request.method == "POST":

        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        ward = request.POST.get("ward")
        reason = request.POST.get("reason")
        priority = request.POST.get("priority")
        doctor_id = request.POST.get("doctor")

        # VALIDATION
        if not name or not age or not doctor_id:

            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": "Name, Age and Doctor are required"
            })

        try:

            doctor = get_object_or_404(
                Doctor,
                id=doctor_id
            )

            Patient.objects.create(
                name=name,
                age=int(age),
                gender=gender or "Unknown",
                phone=phone or "",
                ward=ward or "General",
                reason=reason or "",
                priority=priority or "Normal",
                doctor=doctor
            )

            return redirect("patients")

        except Exception as e:

            print("PATIENT SAVE ERROR:", e)

            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": str(e)
            })

    return render(request, "hospital/reception.html", {
        "doctors": doctors
    })


# ==========================================
# APPOINTMENTS VIEW
# ==========================================
@login_required(login_url='login')
def appointments(request):

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    appointments = Appointment.objects.all().order_by("-id")

    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")

        if not doctor_id or not patient_id:

            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": appointments,
                "error": "Doctor and Patient are required"
            })

        try:

            Appointment.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
                date=request.POST.get("date"),
                time=request.POST.get("time"),
                reason=request.POST.get("reason", "")
            )

            return redirect("appointments")

        except Exception as e:

            print("APPOINTMENT ERROR:", e)

            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": appointments,
                "error": str(e)
            })

    return render(request, "hospital/appointments.html", {
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments
    })


# ==========================================
# PRESCRIPTIONS VIEW
# ==========================================
@login_required(login_url='login')
def prescriptions(request):

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    prescriptions = Prescription.objects.all().order_by("-id")

    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")

        if not doctor_id or not patient_id:

            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions,
                "error": "Doctor and Patient are required"
            })

        try:

            Prescription.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
                medication=request.POST.get("medication"),
                dosage=request.POST.get("dosage"),
                instructions=request.POST.get("instructions")
            )

            return redirect("prescriptions")

        except Exception as e:

            print("PRESCRIPTION ERROR:", e)

            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions,
                "error": str(e)
            })

    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": prescriptions
    })


# ==========================================
# REGISTER VIEW
# ==========================================
def register_view(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:

            error = "Please fill all fields"

        elif User.objects.filter(username=username).exists():

            error = "Username already exists"

        else:

            user = User.objects.create_user(
                username=username,
                password=password
            )

            login(request, user)

            return redirect("dashboard")

    return render(request, "hospital/register.html", {
        "error": error
    })


# ==========================================
# DOCTOR LIST VIEW
# ==========================================
@login_required(login_url='login')
def doctor_list(request):

    doctors = Doctor.objects.all()

    return render(request, "doctors/doctor_list.html", {
        "doctors": doctors
    })


# ==========================================
# ADMIT PATIENT
# ==========================================
@login_required(login_url='login')
def admit_patient(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    # IMPORTANT:
    # Your Patient model MUST contain:
    #
    # is_inpatient = models.BooleanField(default=False)
    # admitted_at = models.DateTimeField(null=True, blank=True)

    patient.is_inpatient = True
    patient.admitted_at = timezone.now()

    patient.save()

    return redirect("reception_dashboard")