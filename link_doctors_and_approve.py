from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Medical.models import Doctors, Booking

class Command(BaseCommand):
    help = 'Link all doctors to User accounts and approve existing bookings'

    def handle(self, *args, **kwargs):
        doctors = Doctors.objects.all()
        for doctor in doctors:
            # Link or create User account
            user, created = User.objects.get_or_create(
                username=doctor.email,
                defaults={'email': doctor.email, 'first_name': doctor.name.split()[0], 'last_name': ' '.join(doctor.name.split()[1:])}
            )
            if created:
                user.set_password('defaultpassword123')  # You can choose a default password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user for doctor {doctor.name}'))

            # Approve all bookings for this doctor
            bookings = Booking.objects.filter(DoctorName=doctor, Approve=False)
            count = bookings.update(Approve=True)
            self.stdout.write(self.style.SUCCESS(f'Approved {count} bookings for doctor {doctor.name}'))

        self.stdout.write(self.style.SUCCESS('All doctors linked and bookings approved!'))
