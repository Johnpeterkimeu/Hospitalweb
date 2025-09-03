from django import forms
from django.contrib.auth.models import User
from .models import Booking, PatientProfile

class PatientRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['phone', 'gender', 'age']

# forms.py

from django import forms
from .models import DoctorAvailability, Doctors 

class BookingForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctors.objects.all(),
        empty_label="-- Select Doctor --",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Booking
        fields = ["doctor", "appointment_date", "appointment_time"]
        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }
class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ApproveBookingForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[('Approved', 'Approve'), ('Rejected', 'Reject')])
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), required=True)

    class Meta:
        # model = AdminApproval
        fields = ['status', 'doctor']