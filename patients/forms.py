from django import forms
from patients.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name',
            'age',
            'gender',
            'symptoms',
            'assigned_doctor',
        ]