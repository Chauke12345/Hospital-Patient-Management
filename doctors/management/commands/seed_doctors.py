from django.core.management.base import BaseCommand
from doctors.models import Doctor

class Command(BaseCommand):
    help = "Seed initial doctors into database"

    def handle(self, *args, **kwargs):

        doctors = [
            ("John", "Smith", "General"),
            ("Amina", "Patel", "Cardiology"),
            ("Thabo", "Mokoena", "Pediatrics"),
        ]

        for first, last, spec in doctors:
            Doctor.objects.get_or_create(
                first_name=first,
                last_name=last,
                specialization=spec,
                phone="0000000000",
                email=f"{first.lower()}@hospital.com"
            )

        self.stdout.write(self.style.SUCCESS("Doctors seeded successfully"))