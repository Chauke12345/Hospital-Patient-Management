from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

# Import models from their OWN apps (correct Django structure)
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from hospital.models import Prescription  # only if it really lives here
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
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("dashboard")

            error = "Invalid username or password"

    return render(request, "hospital/login.html", {
        "error": error
    })


# =====================================
# LOGOUT
# =====================================
def logout_view(request):
    logout(request)
    return redirect("login")


# =====================================
# DASHBOARD
# =====================================
def dashboard(request):

    try:
        context = {
            "total_patients": Patient.objects.count(),
            "total_doctors": Doctor.objects.count(),
            "total_appointments": Appointment.objects.count(),
            "total_prescriptions": Prescription.objects.count(),
        }

    except Exception as e:

        print("DASHBOARD ERROR:", e)

        context = {
            "total_patients": 0,
            "total_doctors": 0,
            "total_appointments": 0,
            "total_prescriptions": 0,
            "error": str(e)
        }

    return render(request, "hospital/dashboard.html", context)


# =====================================
# PATIENTS
# =====================================
def patients(request):

    try:
        patient_list = Patient.objects.all().order_by("-id")

    except Exception as e:

        print("PATIENT ERROR:", e)

        patient_list = []

    return render(request, "hospital/patients.html", {
        "patients": patient_list
    })


# =====================================
# RECEPTION
# =====================================
def reception(request):

    try:
        doctors = Doctor.objects.all()

    except Exception as e:

        print("DOCTOR ERROR:", e)

        doctors = []

    if request.method == "POST":

        try:
            doctor_id = request.POST.get("doctor")

            if not doctor_id:
                return render(request, "hospital/reception.html", {
                    "doctors": doctors,
                    "error": "Please select a doctor"
                })

            doctor = get_object_or_404(Doctor, id=doctor_id)

            Patient.objects.create(
                name=request.POST.get("name", "Unknown"),
                age=int(request.POST.get("age") or 0),
                gender=request.POST.get("gender", "Not specified"),
                phone=request.POST.get("phone", "N/A"),
                ward=request.POST.get("ward", "General"),
                reason=request.POST.get("reason", ""),
                priority=request.POST.get("priority", "Normal"),
                doctor=doctor
            )

            return redirect("patients")

        except Exception as e:

            print("RECEPTION ERROR:", e)

            return render(request, "hospital/reception.html", {
                "doctors": doctors,
                "error": str(e)
            })

    return render(request, "hospital/reception.html", {
        "doctors": doctors
    })


# =====================================
# APPOINTMENTS
# =====================================
def appointments(request):

    try:
        doctors = Doctor.objects.all()
        patient_list = Patient.objects.all()
        appointment_list = Appointment.objects.all()

    except Exception as e:

        print("APPOINTMENT LOAD ERROR:", e)

        doctors = []
        patient_list = []
        appointment_list = []

    if request.method == "POST":

        try:
            Appointment.objects.create(
                doctor_id=request.POST.get("doctor"),
                patient_id=request.POST.get("patient"),
                date=request.POST.get("date"),
                time=request.POST.get("time"),
                reason=request.POST.get("reason", "")
            )

            return redirect("appointments")

        except Exception as e:

            print("APPOINTMENT ERROR:", e)

            return render(request, "hospital/appointments.html", {
                "doctors": doctors,
                "patients": patient_list,
                "appointments": appointment_list,
                "error": str(e)
            })

    return render(request, "hospital/appointments.html", {
        "doctors": doctors,
        "patients": patient_list,
        "appointments": appointment_list
    })


# =====================================
# PRESCRIPTIONS
# =====================================
def prescriptions(request):

    try:
        doctors = Doctor.objects.all()
        patient_list = Patient.objects.all()
        prescription_list = Prescription.objects.all().order_by("-id")

    except Exception as e:

        print("PRESCRIPTION LOAD ERROR:", e)

        doctors = []
        patient_list = []
        prescription_list = []

    if request.method == "POST":

        try:

            patient = Patient.objects.get(
                id=request.POST.get("patient")
            )

            doctor = Doctor.objects.get(
                id=request.POST.get("doctor")
            )

            Prescription.objects.create(
                patient=patient,
                doctor=doctor,
                medication=request.POST.get("medication"),
                dosage=request.POST.get("dosage"),
                instructions=request.POST.get("instructions"),
            )

            return redirect("prescriptions")

        except Exception as e:

            print("PRESCRIPTION ERROR:", e)

            return render(request, "hospital/prescriptions.html", {
                "doctors": doctors,
                "patients": patient_list,
                "prescriptions": prescription_list,
                "error": str(e)
            })

    return render(request, "hospital/prescriptions.html", {
        "doctors": doctors,
        "patients": patient_list,
        "prescriptions": prescription_list
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

    return render(request, "hospital/register.html", {
        "error": error
    })

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors/doctor_list.html", {"doctors": doctors})