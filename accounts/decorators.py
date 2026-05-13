from django.shortcuts import redirect
from functools import wraps

# 🔐 ADMIN ONLY
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != 'ADMIN':
            return redirect('/')

        return view_func(request, *args, **kwargs)
    return wrapper


# 🧑‍⚕️ DOCTOR ONLY
def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != 'DOCTOR':
            return redirect('/')

        return view_func(request, *args, **kwargs)
    return wrapper


# 💊 PHARMACIST ONLY
def pharmacist_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != 'PHARMACIST':
            return redirect('/')

        return view_func(request, *args, **kwargs)
    return wrapper


# 🏥 RECEPTIONIST ONLY
def receptionist_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != 'RECEPTIONIST':
            return redirect('/')

        return view_func(request, *args, **kwargs)
    return wrapper