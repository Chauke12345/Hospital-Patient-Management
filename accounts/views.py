from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required, doctor_required


# -----------------------------
# LOGIN VIEW (ROLE-BASED REDIRECT)
# -----------------------------
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Role-based routing
        if user.role == 'ADMIN':
            return redirect('/')
        elif user.role == 'DOCTOR':
            return redirect('/doctor/')
        elif user.role == 'RECEPTIONIST':
            return redirect('/reception/')
        elif user.role == 'PHARMACIST':
            return redirect('/pharmacy/')
        else:
            return redirect('/')


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