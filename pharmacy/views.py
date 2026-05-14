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