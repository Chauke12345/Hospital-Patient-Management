from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required, doctor_required


# -----------------------------
# LOGIN VIEW (ROLE-BASED REDIRECT)
# -----------------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "hospital/login.html", {"error": error})

# -----------------------------
# LOGOUT
# -----------------------------
def user_logout(request):
    logout(request)
    return redirect('login')


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@login_required
@admin_required
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")


# -----------------------------
# DOCTOR DASHBOARD
# -----------------------------
@login_required
@doctor_required
def doctor_dashboard(request):
    return render(request, 'doctor/dashboard.html')