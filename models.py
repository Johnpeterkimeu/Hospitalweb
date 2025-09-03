from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Doctors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default=None)
    doctor_type = models.CharField(max_length=50)
    contact = models.CharField(max_length=15, default='')
    department = models.CharField(max_length=100, default='')


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.name} - {self.date} {self.start_time} to {self.end_time}"


class Booking(models.Model):
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey("Doctors", on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_bookings'
    )

    # Patient Details
    patient_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField(default=18)
    contact = models.CharField(max_length=20, null=True, blank=True)

    # Appointment Details
    department = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)

    # Status
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        doctor_name = self.doctor.name if self.doctor else "Unassigned"
        return f"{self.patient_name} -> Dr. {doctor_name} @ {self.appointment_date}"


class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=50, default='Pending')
    action = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Appointment for {self.booking.patient_name} ({self.status})"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=30, default='pending')
    assigned_doctor = models.ForeignKey(
        Doctors,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_patients'
    )

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('doctor_approved', 'Doctor Approved'),
        ('admin_approved', 'Admin Approved'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    contact = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name

