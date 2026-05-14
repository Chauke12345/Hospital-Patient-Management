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