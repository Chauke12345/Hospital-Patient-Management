from django.core.management.base import BaseCommand
from doctors.models import Doctor

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        doctors = [
            ("Dr Smith", "General"),
            ("Dr Patel", "Cardiology"),
            ("Dr Mokoena", "Pediatrics"),
            ("Dr Naidoo", "Surgery"),
            ("Dr Dlamini", "Emergency"),
        ]

        for first, spec in doctors:
            Doctor.objects.get_or_create(
                first_name=first.split()[1] if len(first.split()) > 1 else first,
                last_name=first.split()[0] if len(first.split()) > 1 else "",
                specialization=spec,
                phone="0000000000",
                email=f"{first.replace(' ', '').lower()}@hospital.com"
            )

        self.stdout.write("Doctors seeded successfully")