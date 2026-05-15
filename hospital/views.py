from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()

# =========================
# IMPORT MODELS (APP STRUCTURE)
# =========================
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from doctors.models import Prescription


# =========================
# LOGIN VIEW
# Handles user authentication
# =========================
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate input
        if not username or not password:
            error = "Please enter username and password"

        else:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("dashboard")

            error = "Invalid username or password"

    return render(request, "hospital/login.html", {"error": error})


# =========================
# LOGOUT VIEW
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# DASHBOARD VIEW
# Shows system summary
# =========================
def dashboard(request):
    context = {
        "total_patients": Patient.objects.count(),
        "total_doctors": Doctor.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "total_prescriptions": Prescription.objects.count(),
    }
    return render(request, "hospital/dashboard.html", context)


# =========================
# PATIENT LIST VIEW
# =========================
def patient_list(request):
    patients = Patient.objects.all().order_by("-id")
    return render(request, "hospital/patients.html", {"patients": patients})


# =========================
# RECEPTION (REGISTER PATIENT)
# =========================
def reception(request):
    doctors = Doctor.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")

        if not doctor_id:
            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": "Please select a doctor"
            })

        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Create patient safely
        Patient.objects.create(
            name=request.POST.get("name", "Unknown"),
            age=request.POST.get("age") or 0,
            gender=request.POST.get("gender", "Not specified"),
            phone=request.POST.get("phone", ""),
            ward=request.POST.get("ward", "General"),
            reason=request.POST.get("reason", ""),
            priority=request.POST.get("priority", "Normal"),
            doctor=doctor
        )

        return redirect("patients")

    return render(request, "hospital/reception.html", {"doctors": doctors})


# =========================
# APPOINTMENTS VIEW
# =========================
def appointments(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")

        # ✅ Prevent crash if missing form data
        if not doctor_id or not patient_id:
            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": appointments,
                "error": "Doctor and patient are required"
            })

        try:
            Appointment.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
                date=request.POST.get("date"),
                time=request.POST.get("time"),
                reason=request.POST.get("reason", "")
            )

        except Exception as e:
            print("APPOINTMENT ERROR:", e)

            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patients,
                "appointments": appointments,
                "error": str(e)
            })

        return redirect("appointments")

    return render(request, "hospital/appointments.html", {
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments
    })

# =========================
# PRESCRIPTIONS VIEW
# =========================
def prescriptions(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    prescriptions = Prescription.objects.all().order_by("-id")

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        patient_id = request.POST.get("patient")

        # ✅ Prevent missing input crash
        if not doctor_id or not patient_id:
            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions,
                "error": "Doctor and patient are required"
            })

        try:
            Prescription.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id,
                medication=request.POST.get("medication"),
                dosage=request.POST.get("dosage"),
                instructions=request.POST.get("instructions"),
            )

        except Exception as e:
            print("PRESCRIPTION ERROR:", e)

            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": prescriptions,
                "error": str(e)
            })

        return redirect("prescriptions")

    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": prescriptions
    })

# =========================
# REGISTER VIEW
# =========================
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
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("dashboard")

    return render(request, "hospital/register.html", {"error": error})


# =========================
# DOCTOR LIST VIEW
# =========================
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors/doctor_list.html", {"doctors": doctors})

from django.utils import timezone

def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    patient.is_inpatient = True
    patient.admitted_at = timezone.now()
    patient.save()

    return redirect('reception_dashboard')