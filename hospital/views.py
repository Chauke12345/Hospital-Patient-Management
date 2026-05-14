from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from .models import Patient, Doctor, Appointment, Prescription

User = get_user_model()


# =====================================
# LOGIN
# =====================================
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "Please enter username and password"
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                error = "Invalid username or password"

    return render(request, "hospital/login.html", {"error": error})


# =====================================
# LOGOUT
# =====================================
def logout_view(request):
    logout(request)
    return redirect("login")


# =====================================
# DASHBOARD (NO LOGIN REQUIRED)
# =====================================
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("Dashboard works")

# =====================================
# PATIENT LIST
# =====================================
def patients(request):
    return render(request, "hospital/patients.html", {
        "patients": Patient.objects.all().order_by('-id')
    })


# =====================================
# RECEPTION
# =====================================
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

        try:
            Patient.objects.create(
                name=request.POST.get("name") or "Unknown",
                age=int(request.POST.get("age") or 0),
                gender=request.POST.get("gender") or "Not specified",
                phone=request.POST.get("phone") or "N/A",
                ward=request.POST.get("ward") or "General",
                reason=request.POST.get("reason") or "",
                priority=request.POST.get("priority") or "Normal",
                doctor=doctor
            )

            return redirect("patients")

        except Exception as e:
            print("ERROR:", e)

            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": "Error saving patient"
            })

    return render(request, "hospital/reception.html", {
        "doctors": doctors
    })


# =====================================
# APPOINTMENTS
# =====================================
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


# =====================================
# PRESCRIPTIONS
# =====================================
def prescriptions(request):

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")

        try:
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

        except Exception as e:
            print("ERROR:", e)

            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patients,
                "prescriptions": Prescription.objects.all(),
                "error": "Error saving prescription"
            })

    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patients,
        "prescriptions": Prescription.objects.all().order_by("-id")
    })


# =====================================
# REGISTER
# =====================================
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

    return render(request, "hospital/register.html", {"error": error})