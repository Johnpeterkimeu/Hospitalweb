from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import auth
from .models import Booking, Doctors, Patient, DoctorAvailability
from django.contrib.admin.views.decorators import staff_member_required
from .forms import PatientRegisterForm,BookingForm, PatientProfileForm, DoctorAvailabilityForm
from .models import PatientProfile
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from .forms import ApproveBookingForm
from django.views.decorators.http import require_POST
from datetime import datetime
import africastalking
from django.core.mail import send_mail
from django.conf import settings




    # Create your views here.
    # Notification logic

#      def send_sms_notification(phone_number, message):
#         africastalking.initialize(
#             username=settings.AFRICASTALKING_USERNAME,
#             api_key=settings.AFRICASTALKING_API_KEY
#         )
# sms = africastalking.SMS
#         sms.send(message, [phone_number])

#     def send_notifications(booking):
#         patient = booking.patient
#         doctor = booking.doctor

        # patient_email = patient.email if patient else None
        # patient_phone = booking.Contact
        # patient_msg = f"Hi {booking.PatientName}, your appointment has been approved and assigned to Dr. {doctor.Name}."

        # doctor_email = doctor.Email
        # doctor_phone = doctor.phone
        # doctor_msg = f"You have a new patient assigned: {booking.PatientName}."

        # # Send email
        # if patient_email:
        #     send_mail("Appointment Approved", patient_msg, settings.DEFAULT_FROM_EMAIL, [patient_email])
        # if doctor_email:
        #     send_mail("New Patient Assigned", doctor_msg, settings.DEFAULT_FROM_EMAIL, [doctor_email])

        # # Send SMS
        # if patient_phone:
        #     send_sms_notification(patient_phone, patient_msg)
        # if doctor_phone:
        #     send_sms_notification(doctor_phone, doctor_msg)


def Home(request):
        return render(request,'index.html')
def About(request):
    return render(request,'about.html')
def Services(request):
    return render(request,'serv.html')
def Departments(request):
    return render(request,'departments.html') 

@login_required
# @user_passes_test(is_admin)
def admin_pending_bookings(request):
    pending_bookings = Booking.objects.filter(is_approved=False)
    return render(request, 'pending_bookings.html', {'bookings': pending_bookings})

@login_required
# @user_passes_test(is_admin)
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    approval, created = AdminApproval.objects.get_or_create(booking=booking)

    if request.method == 'POST':
        form = ApproveBookingForm(request.POST, instance=approval)
        if form.is_valid():
            approval = form.save(commit=False)
            booking.doctor = form.cleaned_data['doctor']
            booking.is_approved = (form.cleaned_data['status'] == 'Approved')
            booking.save()
            approval.save()
            return redirect('admin_pending_bookings')  # Adjust as needed
        else:
            form = ApproveBookingForm(instance=approval)

        return render(request, 'approve_booking.html', {
            'form': form,
            'booking': booking
        })

    def Admin(request):
        if request.method == 'POST':
            admin_id = request.POST.get('AdminID') 
            password = request.POST.get('Password')   

            user = authenticate(request, username=admin_id, password=password)

            if user is not None:
                if user.is_staff:
                    login(request, user)
                    print(" User is authenticated and is staff.")
                    messages.success(request, "Login successful.")
                    return redirect('AdminBash')  # Use redirect instead of render
                else:
                    print("User is not a staff member.")
                    messages.error(request, "You do not have admin privileges.")
                    return render(request, 'Admin1.html')
            else:
                print("Invalid credentials.")
                messages.error(request, "Invalid credentials.")
                return render(request, 'Admin1.html')

        # GET request
        return render(request, 'Admin1.html')
        
    
        

    def Admin_Table(request):
        doctors = Appointments.objects.all()  # Assuming you want to fetch all doctors from the Appointments model
        return render(request, 'AdminDoctors.html', {'doctors': doctors})
            
    def is_admin(user):
        return user.is_authenticated and user.is_staff
    def is_admin(user):
        return user.is_authenticated and user.is_staff
    def is_admin(user):
        return user.groups.filter(name='Admin').exists()

@login_required
# @user_passes_test(is_admin)
def approve_booking(request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        approval, created = AdminApproval.objects.get_or_create(booking=booking)

        if request.method == 'POST':
            form = ApproveBookingForm(request.POST, instance=approval)
            if form.is_valid():
                approval = form.save(commit=False)
                booking.doctor = form.cleaned_data['doctor']
                booking.is_approved = (form.cleaned_data['status'] == 'Approved')
                booking.save()
                approval.save()
                return redirect('Admin_Appointments')  # Adjust as needed
        else:
            form = ApproveBookingForm(instance=approval)

        return render(request, 'approve_booking.html', {
            'form': form,
            'booking': booking
        })
# @user_passes_test(is_admin)
def admin_pending(request):
        pending_bookings = Booking.objects.filter(is_approved=False)
        return render(request, 'pending_bookings.html', {'bookings': pending_bookings})
def PatientRecord(request):
        return render(request, 'PatientRecordDashboard.html')
def DashboardAdmin(request):
        return render(request, 'AdminDashboard.html')

def AdminDashboard(request):
        doctors = Doctors.objects.all()
        return render(request, 'AdminDashboard1.html', {'doctors': doctors})

def AdminPatientView(request):
        patients = Patient.objects.all()
        
        return render(request, 'AdminPatient.html', {'patients': patients})


def DoctorsPage(request):
        
    return render(request,'Drd.html')
def DoctorsList(request):
        status = request.GET.get('status')

        if status == 'available':
            doctors = Doctors.objects.filter(status='available')
        elif status == 'leave':
            doctors = Doctors.objects.filter(status='leave')
        else:
            doctors = Doctors.objects.all()

        return render(request, 'AdminDoctors.html', {'doctors': doctors})

def AllDoctors(request):
            doctors = Doctors.objects.all()
            return render(request, 'AllDoctors.html', {'doctors': doctors})

def AvailableDoctors(request):
        doctors = Doctors.objects.filter(status='available')  # Use correct field name
        return render(request, 'AvailableDoctors.html', {'doctors': doctors})  # Use correct variable

def BookingView(request):
        return render(request,'BookingAppointments1.html')
@login_required
def BookingAppointment(request):
        if request.method == 'POST':
            patient_name = request.POST.get('patientName')
            gender = request.POST.get('Gender')
            age = request.POST.get('Age')
            contact = request.POST.get('Phone')
            doctor = request.POST.get('Doctor')
            appointment_date = request.POST.get('Date')

            if not appointment_date:
                messages.error(request, "Date is required.")
                return redirect('Booking_Appoint')  # Stay on form if error
            if contact.startswith("0"):
             contact = "+254" + contact[1:]
            elif contact.startswith("7"):
                contact = "+254" + contact
            elif not contact.startswith("+"):
                contact = "+254" + contact  # fallback
            # Save Booking
            booking = Booking.objects.create(
                PatientName=patient_name,
                Gender=gender,
                Age=age,
                Contact=contact,
                appointment_date=date,  # Assuming your Booking model has this field
                Doctor=doctor  # If your Booking model has a doctor field
            )

            #  Save to Patient (if needed)
            patient = Patient.objects.create(
                name=patient_name,
                gender=gender,
                age=age,
                contact=contact,
                date=date,
                doctor=doctor
            )

            messages.success(request, "Appointment booked successfully.")
            return redirect('BookingList')

        return render(request, 'AppointmentsForm.html')
def BookingList(request):
        return render(request, 'BookingList.html')

# @user_passes_test(is_admin)
def Admin_Approved(request):
        if request.method == 'POST':
            patient_id = request.POST.get('patient_id')
            doctor_id = request.POST.get('assigned_doctor')

            patient = get_object_or_404(Patient, id=patient_id)
            doctor = get_object_or_404(Doctors, id=doctor_id)

            patient.status = 'admin_approved'
            patient.doctor = doctor
            patient.save()

            # Optional SMS or email logic here...

            messages.success(request, f"Patient {patient.name} approved and assigned to {doctor.Name}.")
            return redirect('AdminApproval')

        pending_patients = Patient.objects.filter(status='pending')
        doctors = Doctors.objects.filter(status='available')  # or all if no filter
        return render(request, 'AdminApproval.html', {
            'pending_patients': pending_patients,
            'doctors': doctors
        })
@login_required
def DoctorAssignedPatients(request):
        if not hasattr(request.user, 'doctors'):
            messages.error(request, "You are not a doctor.")
            return redirect('DoctorsDashboard')

        doctor = request.user.doctors
        assigned_patients = Patient.objects.filter(doctor=doctor, status='admin_approved')

        return render(request, 'DoctorPatientsList.html', {'patients': assigned_patients})

@login_required
def DoctorApprovePatients(request):
        if request.method == 'POST':
            patient_id = request.POST.get('patient_id')
            try:
                patient = Patient.objects.get(id=patient_id)
                patient.status = 'doctor_approved'
                patient.save()

                # Email notification to patient
                send_mail(
                    subject='Doctor Approval Notification',
                    message=f'Dear {patient.name}, you have been approved by a doctor and are awaiting admin approval.',
                    from_email='hospital@system.com',
                    recipient_list=[patient.contact + '@your-sms-gateway.com'],  # replace with actual email or SMS format
                    fail_silently=True
                )

                messages.success(request, f"Patient '{patient.name}' approved and notified.")
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found.")

        pending_patients = Patient.objects.filter(status='pending')
        return render(request, 'DoctorsApproval.html', {'pending_patients': pending_patients})
@staff_member_required
def Admin_Approves(request):
        if request.method == 'POST':
            doctor_approved_patients = Patient.objects.filter(status='doctor_approved')
            updated_count = 0

            for patient in doctor_approved_patients:
                patient.status = 'admin_approved'
                patient.save()
                updated_count += 1

                # Notify patient of final approval
                send_mail(
                    subject='Appointment Final Approval',
                    message=f'Dear {patient.name}, your appointment request has been approved by the admin. You can now proceed.',
                    from_email='hospital@system.com',
                    recipient_list=[patient.contact + '@your-sms-gateway.com'],  # or actual email
                    fail_silently=True
                )

            messages.success(request, f"{updated_count} patient(s) approved and notified.")
            return redirect('AdminApproval')

        doctor_approved_patients = Patient.objects.filter(status='doctor_approved')
        return render(request, 'AdminApproval.html', {'patients': doctor_approved_patients})

@staff_member_required
def Admin_Approve(request, patient_id):
        if request.method == 'POST':
            patient = get_object_or_404(Patient, id=patient_id)
            patient.status = 'admin_approved'
            patient.save()
            messages.success(request, f"{patient.name} has been approved.")
        return redirect('AdminApproval')
@login_required
@require_POST
def ApproveByDoctor(request):
        patient_id = request.POST.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.status = 'doctor_approved'  # Temporary until admin confirms
            patient.save()
            messages.success(request, f"Patient {patient.name} approved and sent to admin.")
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found.")
        return redirect('DoctorsApproval')

def RegisterPatients(request):
        if request.method == 'POST':
            user_form = PatientRegisterForm(request.POST)
            profile_form = PatientProfileForm(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)  # hash the password
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Account created successfully.")
                return redirect('Login')  
                print("LOGIN SUCESSIFUL")

            else:
                messages.error(request, "Please fix the form errors below.")
                print("LoginUNSUSESSifull")
        else:
            user_form = PatientRegisterForm()
            profile_form = PatientProfileForm()

    
        return render(request, 'RegisterPatient.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

def Login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('Booking_Appoint')  # or your actual redirect URL
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('Login')  # stay on login page

        return render(request, 'login.html')  # handles GET request
def logout(request):
        return redirect('login')

@login_required
def PatientDashboard(request):
        profile = PatientProfile.objects.get(user=request.user)
        return render(request, 'AppointmentsForm.html', {'profile': profile})

@login_required
def DoctorApprovePatients(request):
        if request.method == 'POST':
            patient_id = request.POST.get('patient_id')
            patient = get_object_or_404(Patient, id=patient_id)
            patient.status = 'Approved'
            patient.save()
            messages.success(request, f"Patient '{patient.name}' approved successfully.")

        pending_patients = Patient.objects.filter(status='pending')
        return render(request, 'DoctorsApproval.html', {
            'pending_patients' : pending_patients 
            })


@login_required
def BookingViewAppointment(request):
        # Fetch appointments only for the currently logged-in user
        appointments = Appointments.objects.filter(patient=request.user)
        return render(request, 'BookingList.html', {'appointments': appointments})

def BookingTable(request):
        appointment = Appointments.objects.all()
        bookings =  Booking.objects.all()
    
        return render(request, 'AppointmnetsTable.html', {
            'appointments': appointment,
            'bookings': bookings
        
            }
                    )
def SubmitAppointment(request):
        if request == 'POST':
            PatientName = request.POST.get('patientName')
            
def Adminview(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username == '1' and password == '123456':
            
                return redirect('Adminpage.html')
            else:
                return HttpResponse("Invalid credentials")
        return render(request,'Admin1.html')
def AdminDoctors(request):
        doctors = Doctors.objects.all()  # Fetch all doctors from the database
        return render(request, 'AdminDoctors.html', {'doctors': doctors})
        
def AdminPatient(request):
        return render(request, 'AdminpatientManagement.html')

def Admin(request):
        if request.method == 'POST':
            admin_id = request.POST.get('AdminID') 
            password = request.POST.get('Password')   

            user = authenticate(request, username=admin_id, password=password)

            if user is not None:
                if user.is_staff:
                    login(request, user)
                    print(" User is authenticated and is staff.")
                    messages.success(request, "Login successful.")
                    return redirect('AdminBash')  # Use redirect instead of render
                else:
                    print("User is not a staff member.")
                    messages.error(request, "You do not have admin privileges.")
                    return render(request, 'Admin1.html')
            else:
                print("Invalid credentials.")
                messages.error(request, "Invalid credentials.")
                return render(request, 'Admin1.html')

        # GET request
        return render(request, 'Admin1.html')
        
        

def Admin_Table(request):
        doctors = Appointments.objects.all()  # Assuming you want to fetch all doctors from the Appointments model
        return render(request, 'AdminDoctors.html', {'doctors': doctors})
            
def is_admin(user):
        return user.is_authenticated and user.is_staff
@user_passes_test(is_admin)
def PatientRecord(request):
        return render(request, 'PatientRecordDashboard.html')
def DashboardAdmin(request):
        return render(request, 'AdminDashboard.html')

def AdminDashboard(request):
        doctors = Doctors.objects.all()
        return render(request, 'AdminDashboard1.html', {'doctors': doctors})

def AdminPatientView(request):
        patients = Patient.objects.all()
        
        return render(request, 'AdminPatient.html', {'patients': patients})

def Staff(request):
        staff_id = None
        password = None
        Email = None
        if request.method == 'POST':
                staff_id = request.POST.get('Username or Registration ID')
                password = request.POST.get('pcd assword')
                Email = request.POST.get('Email')
                # Here you would typically check the credentials against the database
        user = authenticate(staff_id='Username', password=password) 
        if user is not None:
                    messages.success(request, 'Login successful')
                    print("Login successful")
                    return redirect('StaffDetails') 
        else:  
            messages.warning(request, "Invalid credentials")
            print("Invalid credentials") 
                # If the credentials are invalid, you can render the login page again with an error message
                
                
        return render(request,'stafflogin1.html', {'staff_id': staff_id, 'password': password, 'Email': Email})
def StaffDetails(request):
        if request.method == 'POST':
            staff_id = request.POST.get('StaffID')
            username = request.POST.get('Username')
            department = request.POST.get('Department')
            contact = request.POST.get('Contact')
            email = request.POST.get('Email')
            # Here you would typically save the staff details to the database
            # For now, we will just return a success message
        
        return render(request, 'staffdetails.html')
def DoctorsPage(request):
        
    return render(request,'Drd.html')

def DoctorsList(request):
        status = request.GET.get('status')

        if status == 'available':
            doctors = Doctors.objects.filter(status='available')
        elif status == 'leave':
            doctors = Doctors.objects.filter(status='leave')
        else:
            doctors = Doctors.objects.all()

        return render(request, 'AdminDoctors.html', {'doctors': doctors})

def AllDoctors(request):
            doctors = Doctors.objects.all()
            return render(request, 'AllDoctors.html', {'doctors': doctors})

def AvailableDoctors(request):
        doctors = Doctors.objects.filter(status='available')  # Use correct field name
        return render(request, 'AvailableDoctors.html', {'doctors': doctors})  # Use correct variable

def BookingView(request):
        return render(request,'BookingAppointments1.html')
def approve_booking(request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Approved'
        booking.save()
        messages.success(request, f"Appointment for {booking.PatientName} has been approved.")
        return redirect('Admin_Appointments')  # make sure this matches your URL name def approvalAppointment(request, id):
        appointment = Appointments.objects.get(AppointmentID=id)
        appointment.Status = 'Approved'
        appointment.Action = 'Approved by Admin'
        appointment.save()
        return redirect('Admin_Appointments')

def rejectAppointment(request, id):
        appointment = Appointments.objects.get(AppointmentID=id)
        appointment.Status = 'Rejected'
        appointment.Action = 'Rejected by Admin'
        appointment.save()
        return redirect('Admin_Appointments')

@login_required
def PatientBookings(request):
        # Filter bookings using the logged-in user's username
        username = request.user.username  # Adjust if you use a different field
        bookings = Booking.objects.filter(PatientName=username)

        bookings_list = []
        for booking in bookings:
            status = 'Approved' if getattr(booking, 'is_approved', False) else 'Pending'
            bookings_list.append({'booking': booking, 'status': status})

        context = {
            'bookings': bookings_list,
        }
        return render(request, 'PatientBookingList.html', context)
@login_required
def BookingAppointment(request):
        if request.method == 'POST':
            patient = request.user
            doctor_id = request.POST.get('doctor_id')
            patient_name = request.POST.get('patient_name')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            contact = request.POST.get('contact')
            department = request.POST.get('department')
            specialization = request.POST.get('specialization')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
        
            if not appointment_date:
                messages.error(request, "Date is required.")
                return redirect('Booking_Appoint')  # Stay on form if error
            if contact.startswith("0"):
               contact = "+254" + contact[1:]
            elif contact.startswith("7"):
                contact = "+254" + contact
            elif not contact.startswith("+"):
                contact = "+254" + contact  # fallback
            # Save Booking
            booking = Booking.objects.create(
            patient=request.user,
            patient_name=profile.user.get_name() or profile.user.username,
            gender=profile.gender,
            age=profile.age,
            contact=profile.phone,
            doctor=doctor,
            department=doctor.department,
            specialization=doctor.doctor_type,
            appointment_date=slot.date,
            appointment_time=slot.start_time,
        )

            #  Save to Patient (if needed)
            Patient.objects.create(
            name=patient_name,
            gender=gender,
            age=age,
            contact=contact,
            doctor=doctor,
        )
        # views.py


        if request.method == 'POST':
            doctor_id = request.POST.get('doctor')
            slot_id = request.POST.get('slot')

            doctor = Doctors.objects.get(id=doctor_id)
            slot = DoctorAvailability.objects.get(id=slot_id)

            if slot.is_booked:
                messages.error(request, "This slot has already been booked.")
                return redirect('Booking_Appoint')

            # Get the patient's profile
            profile = PatientProfile.objects.get(user=request.user)
            # Create appointment
            Booking.objects.create(
                patient=request.user,
                PatientName=profile.user.get_name() or profile.user.username,
                Gender=profile.gender,
                Age=profile.age,
                Contact=profile.phone,
                Doctor=doctor.Name,
                DoctorName=doctor.Name,
                Department=doctor.Department,
                Specialization=doctor.doctor_type,
                doctor=doctor,
                Date=slot.date,
                date=datetime.combine(slot.date, slot.start_time),  # combined datetime
                time=slot.start_time,
            )

            # Mark slot as booked
            slot.is_booked = True
            slot.save()

            messages.success(request, "Appointment booked successfully.")
            return redirect('patientBookings')

        doctors = Doctors.objects.all()
        available_slots = DoctorAvailability.objects.filter(is_booked=False)

        return render(request, 'AppointmentsForm.html', {
            'doctors': doctors,
            'slots': available_slots,
        })

        messages.success(request, "Appointment booked successfully.")
        return redirect('patientBookings')

        return render(request, 'AppointmentsForm.html')
def BookingList(request):
        return render(request, 'BookingList.html')

@login_required
def booking_appointment(request):
        if request.method == 'POST':
            patient = request.user
            doctor_id = request.POST.get('doctor_id')
            patient_name = request.POST.get('patient_name')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            contact = request.POST.get('contact')
            department = request.POST.get('department')
            specialization = request.POST.get('specialization')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

            try:
                doctor = Doctors.objects.get(id=doctor_id)
            except Doctors.DoesNotExist:
                messages.error(request, "Selected doctor not found.")
                return redirect('booking_appointment')

            booking = Booking.objects.create(
                patient=patient,
                doctor=doctor,
                patient_name=patient_name,
                gender=gender,
                age=age,
                contact=contact,
                department=department,
                specialization=specialization,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            )
            messages.success(request, "Your appointment request has been submitted.")
            return redirect('Booking_Appoint')

        # GET: render booking form with list of doctors
        doctors = Doctors.objects.all()
        return render(request, 'AppointmentsForm.html', {'doctors': doctors})

@user_passes_test(is_admin)
def Admin_Approved(request):
        if request.method == 'POST':
            patient_id = request.POST.get('patient_id')
            doctor_id = request.POST.get('assigned_doctor')

            patient = get_object_or_404(Patient, id=patient_id)
            doctor = get_object_or_404(Doctors, id=doctor_id)

            patient.status = 'admin_approved'
            patient.doctor = doctor
            patient.save()

            # Optional SMS or email logic here...

            messages.success(request, f"Patient {patient.name} approved and assigned to {doctor.Name}.")
            return redirect('AdminApproval')

        pending_patients = Patient.objects.filter(status='pending')
        doctors = Doctors.objects.filter(status='available')  # or all if no filter
        return render(request, 'AdminApproval.html', {
            'pending_patients': pending_patients,
            'doctors': doctors
        })


@login_required
def Doctor_Availability(request):
        # doctor = Doctors.objects.get(email=request.user.email)
        
        if request.method == 'POST':
            form = DoctorAvailabilityForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Availability successfully allocated.")
                return redirect('allocate_doctor')  # change to your URL name
        else:
            form = DoctorAvailabilityForm()
        
        return render(request, 'DoctorAllocation.html', {'form': form})

@staff_member_required  # only admins/staff can access
def Admin_Appointments(request):
        bookings = Booking.objects.all()
        return render(request, 'AdminApointments.html', {'bookings': bookings})


        # bookings = Booking.objects.all().order_by('-id')
        
        # booking = get_object_or_404(Booking, pk=booking_id)
        # booking.status = "Approved"
        # booking.save()

        # # Send SMS notification
        # phone = booking.Contact  # Replace with actual phone field name
        # message = f"Dear {booking.PatientName}, your appointment has been approved. Please come for review."

        context = {
            'bookings': bookings
        }
        return render(request, 'AdminApointments.html', context)


def review_patient_view(request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        # Optional: Check that this booking belongs to the logged-in doctor
        doctor_name = request.session.get('doctor_name')
        if booking.DoctorName != doctor_name:
            return render(request, 'error.html', {'message': 'Unauthorized access.'})

        return render(request, 'review_patient.html', {'booking': booking})

@login_required
def assigned_patients(request):
        doctor = get_object_or_404(Doctors, user=request.user)

        bookings = Booking.objects.filter(
            doctor=doctor,
            adminapproval__status='Approved'
        ).select_related('doctor', 'adminapproval')

        return render(request, 'Allocated.html', {
            'approved_patients': bookings,
            'doctor': doctor
        })
        # try:
        #     # Get the logged-in doctor's profile
        #     doctor = Doctors.objects.get(user=request.user)
        #     print(f"[DEBUG] Logged-in doctor: {doctor.Name} (ID: {doctor.id})")

        #     # Fetch bookings that are approved by admin and assigned to this doctor
        #     bookings = Booking.objects.filter(
        #         doctor=doctor,
        #         adminapproval__status='Approved'
        #     ).select_related('doctor', 'adminapproval')

        #     print(f"[DEBUG] Total approved bookings found: {bookings.count()}")
        #     for b in bookings:
        #         print(f" - Patient: {b.PatientName}, Date: {b.Date}, Time: {b.time}, Contact: {b.Contact}")

        # except Doctors.DoesNotExist:
        #     print(f"[ERROR] Doctor profile not found for user: {request.user.username}")
        #     return render(request, 'Allocated.html', {
        #         'error': 'Doctor profile not found. Please contact admin.'
        #     })

        # if not bookings.exists():
        #     print(f"[INFO] No approved bookings found for Dr. {doctor.Name}.")

        # return render(request, 'Allocated.html', {
        #     'approved_patients': bookings,
        #     'doctor': doctor
        # })
@login_required
def Doctor_patients(request):
    doctor_name = request.user.first_name  # or username, depending on your system

    approved_bookings = Booking.objects.filter(
            DoctorName=doctor_name,
            adminapproval__status='Approved'  # if 'adminapproval_set' causes problems, try this
        )

    context = {
        'bookings': approved_bookings
    }
    return render(request, 'Allocated.html', context)

    @login_required
    def doctor_approved_patients(request):
        doctor_email = request.user.email.strip().lower()

        try:
            doctor = Doctors.objects.get(Email__iexact=doctor_email)
        except Doctors.DoesNotExist:
            return render(request, 'approved_patients.html', {
                'error': 'Doctor profile not found in the system.'
            })
            
            
        print("User email:", request.user.email)
        print("Doctor emails in DB:", list(Doctors.objects.values_list("Email", flat=True)))

        approved_patients = Booking.objects.filter(
            DoctorName=doctor.Name,
            adminapproval__status='Approved'  # Assuming 'adminapproval__status' is the
            # is_approved=True
        )

        return render(request, 'approved_patients.html', {
            'doctor': doctor,
            'patients': approved_patients
        })
    @login_required
    def doctor_approved_appointments(request):
        try:
            # Get the doctor object linked to the currently logged-in user
            doctor = Doctors.objects.get(user=request.user)

            # Fetch all bookings for this doctor where admin approval is 'Approved'
            bookings = Booking.objects.filter(
                doctor=doctor,
                adminapproval__status='Approved'
            ).select_related('adminapproval')

        except Doctors.DoesNotExist:
            bookings = []  # If doctor profile doesn't exist, show nothing

        context = {
            'bookings': bookings
        }
        return render(request, 'doctor/approved_patients.html', context)
    # @login_required
    # def assigned_patients(request):
    #     try:
    #         doctor = Doctors.objects.get(user=request.user)
    #     except Doctors.DoesNotExist:
    #         messages.error(request, "You are not registered as a doctor.")
    #         return redirect('DoctorAssign')  # Or another appropriate page

    #     # Now filter approved bookings
    #     bookings = Booking.objects.filter(
    #         DoctorName=doctor.full_name,
    #         adminapproval__Approve=True
    #     )
    #     return render(request, 'Allocated.html', {'bookings': bookings})

    







    # Ask ChatGPT


    @staff_member_required
    @login_required
    def approve_booking(request):
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')

            # Make sure booking ID is valid
            booking = get_object_or_404(Booking, id=booking_id)

            # Mark the booking as approved
            booking.is_approved = True
            booking.save()

            # Link to doctor in PatientProfile (optional)
            try:
                profile = PatientProfile.objects.get(user=booking.patient)
                profile.assigned_doctor = booking.doctor.user
                profile.save()
            except PatientProfile.DoesNotExist:
                messages.warning(request, "Patient profile not found. Booking approved anyway.")

            messages.success(request, "Booking approved successfully.")
            return redirect('Admin_Appointments')  
def DoctorAssignedPatients(request):
        try:
            doctor = Doctors.objects.get(Email=request.user.email)
            patients = Booking.objects.filter(doctor=doctor)
        except Doctors.DoesNotExist:
            return render(request, 'DoctorPatientList.html', {
                'error': 'Doctor profile not found for the logged-in user.'
            })

        return render(request, 'DoctorPatientList.html', {
            'doctor': doctor,
            'patients': patients
        })

@login_required
def DoctorApprovePatients(request):
        if request.method == 'POST':
            patient_id = request.POST.get('patient_id')
            try:
                patient = Patient.objects.get(id=patient_id)
                patient.status = 'doctor_approved'
                patient.save()

                # Email notification to patient
                send_mail(
                    subject='Doctor Approval Notification',
                    message=f'Dear {patient.name}, you have been approved by a doctor and are awaiting admin approval.',
                    from_email='hospital@system.com',
                    recipient_list=[patient.contact + '@your-sms-gateway.com'],  # replace with actual email or SMS format
                    fail_silently=True
                )

                messages.success(request, f"Patient '{patient.name}' approved and notified.")
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found.")

        pending_patients = Patient.objects.filter(status='pending')
        return render(request, 'DoctorsApproval.html', {'pending_patients': pending_patients})
@staff_member_required
def Admin_Approves(request):
        if request.method == 'POST':
            doctor_approved_patients = Patient.objects.filter(status='doctor_approved')
            updated_count = 0

            for patient in doctor_approved_patients:
                patient.status = 'admin_approved'
                patient.save()
                updated_count += 1

                # Notify patient of final approval
                send_mail(
                    subject='Appointment Final Approval',
                    message=f'Dear {patient.name}, your appointment request has been approved by the admin. You can now proceed.',
                    from_email='hospital@system.com',
                    recipient_list=[patient.contact + '@your-sms-gateway.com'],  # or actual email
                    fail_silently=True
                )

            messages.success(request, f"{updated_count} patient(s) approved and notified.")
            return redirect('AdminApproval')

        doctor_approved_patients = Patient.objects.filter(status='doctor_approved')
        return render(request, 'AdminApproval.html', {'patients': doctor_approved_patients})

@staff_member_required
def Admin_Approve(request, patient_id):
        if request.method == 'POST':
            patient = get_object_or_404(Patient, id=patient_id)
            patient.status = 'admin_approved'
            patient.save()
            messages.success(request, f"{patient.name} has been approved.")
        return redirect('AdminApproval')
@login_required
@require_POST
def ApproveByDoctor(request):
        patient_id = request.POST.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.status = 'doctor_approved'  # Temporary until admin confirms
            patient.save()
            messages.success(request, f"Patient {patient.name} approved and sent to admin.")
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found.")
        return redirect('DoctorsApproval')

def RegisterPatients(request):
        if request.method == 'POST':
            user_form = PatientRegisterForm(request.POST)
            profile_form = PatientProfileForm(request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)  # hash the password
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Account created successfully.")
                return redirect('Login')  
                print("LOGIN SUCESSIFUL")

            else:
                messages.error(request, "Please fix the form errors below.")
                print("LoginUNSUSESSifull")
        else:
            user_form = PatientRegisterForm()
            profile_form = PatientProfileForm()

    
        return render(request, 'RegisterPatient.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

def Login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('book_appointment')  # or your actual redirect URL
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('Login')  # stay on login page

        return render(request, 'login.html')  # handles GET request
def logout(request):
        return redirect('login')

@login_required
def PatientDashboard(request):
        profile = PatientProfile.objects.get(user=request.user)
        return render(request, 'AppointmentsForm.html', {'profile': profile})
@login_required
def DoctorApprovePatients(request):
        if request.method == 'POST':
            patient_id = request.POST.get('patient_id')
            patient = get_object_or_404(Patient, id=patient_id)
            patient.status = 'Approved'
            patient.save()
            messages.success(request, f"Patient '{patient.name}' approved successfully.")

        pending_patients = Patient.objects.filter(status='pending')
        return render(request, 'DoctorsApproval.html', {
            'pending_patients' : pending_patients 
            })


@login_required
def BookingViewAppointment(request):
        # Fetch appointments only for the currently logged-in user
        appointments = Appointments.objects.filter(patient=request.user)
        return render(request, 'BookingList.html', {'appointments': appointments})

def BookingTable(request):
        appointment = Appointments.objects.all()
        bookings =  Booking.objects.all()
    
        return render(request, 'AppointmnetsTable.html', {
            'appointments': appointment,
            'bookings': bookings
        
            }
                    )
def SubmitAppointment(request):
        if request == 'POST':
            PatientName = request.POST.get('patientName')
            
def Adminview(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username == '1' and password == '123456':
            
                return redirect('Adminpage.html')
            else:
                return HttpResponse("Invalid credentials")
        return render(request,'Admin1.html')
def AdminDoctors(request):
        doctors = Doctors.objects.all()  # Fetch all doctors from the database
        return render(request, 'AdminDoctors.html', {'doctors': doctors})
        
def AdminPatient(request):
        return render(request, 'AdminpatientManagement.html')

def doctor_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # authenticate from Doctors table
            doctor = Doctors.objects.get(email=email, password=password)

            # store doctor info in session
            request.session["doctor_id"] = doctor.id
            request.session["doctor_name"] = doctor.name

            messages.success(request, f"Welcome {doctor.name}!")
            return redirect("Doctor_Dashboard")  # update with your dashboard URL name

        except Doctors.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("doctor_login")

    return render(request, "doctorse.html")  # ✅ uses doctor
def Dashboard_Doctor(request):
        return render(request, 'Dashboard.Doctor.html')

def DoctorsDashboard(request):
    doctors = Doctors.objects.all()
    selected_doctor_id = request.GET.get('doctor_id')
    reports = []

    if selected_doctor_id:
            reports = Booking.objects.select_related('doctor', 'patient').filter(doctor_id=selected_doctor_id)

    return render(request, 'doctor_dashboard.html', {
            'doctors': doctors,
            'reports': reports,
            'selected_doctor_id': selected_doctor_id
    })
def register_doctor(request):
    if request.method == "POST":
        name = request.POST.get("name")  # full name input
        email = request.POST.get("email")
        password = request.POST.get("password")
        doctor_type = request.POST.get("doctor_type")

        # Split full name (if you want first/last)
        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        # 1. Create User
        user = User.objects.create(
            username=email.split("@")[0],
            email=email,
            is_staff=True,
            is_active=True,
            password=make_password(password)
        )

        # 2. Create Doctors profile linked to User
        try:
            doctor = Doctors.objects.create(
                user=user,
                doctor_type=doctor_type
            )

            messages.success(request, f"Doctor {name} registered successfully.")
            return redirect("register_doctor")
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("register_doctor")

    return render(request, "register_doctor.html")
def DoctorAuth(request):
        if request.method == 'POST':
            if 'register' in request.POST:
                # Registration logic
                name = request.POST.get('Name')
                email = request.POST.get('Email')
                phone = request.POST.get('phone')
                doctor_type = request.POST.get('doctor_type')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                department = request.POST.get('Department')

                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('DoctorAuth')

                if Doctors.objects.filter(Email=email).exists():
                    messages.error(request, "A doctor with this email already exists.")
                    return redirect('DoctorAuth')

                doctor = Doctors.objects.create(
                    Name=name,
                    Email=email,
                    password=password,
                    doctor_type=doctor_type,
                    phone=phone,
                    Department=Department,
                    status='available'
                )
                doctor.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('DoctorAuth')

            elif 'login' in request.POST:
                # Login logic
                email = request.POST.get('email')
                password = request.POST.get('Password')

                try:
                    doctor = Doctors.objects.get(Email=email)
                    if doctor.password == password:
                        request.session['doctor_id'] = doctor.id
                        messages.success(request, f"Welcome Dr. {doctor.Name}")
                        return redirect('DoctorDashboard')
                    else:
                        messages.error(request, "Incorrect password.")
                except Doctors.DoesNotExist:
                    messages.error(request, "No doctor found with that email.")

        return render(request, 'doctor_auth.html')
def doctors_registration(request):
        if request.method == 'POST':
            doctor_id = request.POST.get('doctor_id')
            password = request.POST.get('password')
            # Here you would typically save the doctor details to the database
            # For now, we will just return a success message
            return HttpResponse(f"Doctor {doctor_id} registered successfully with password {password}")
        return render(request, 'Doctors.registration.html')
def DoctorsPatientRecords(request):
        return render(request,'PatientRecords.html')
def Main_Doctors(request):
        doctors = Doctors.objects.all()
        return render(request, 'doctors.main.html', {'Doctors': doctors})
def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctors_registration')

    doctor = Doctors.objects.get(id=doctor_id)

    # Handle availability submission from doctor_allocation.html
    if request.method == "POST":
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        is_available = request.POST.get("is_available") == "on"

        DoctorAvailability.objects.create(
            doctor=doctor,
            date=date,
            start_time=start_time,
            end_time=end_time,
            is_available=is_available
        )
        messages.success(request, "Availability updated successfully!")
        return redirect("Doctor_Dashboard")

    # Patients scheduled (approved bookings)
    scheduled_patients = Booking.objects.filter(
    doctor=doctor,
    is_approved=True   # or adminapproval__Approve=True depending on your setup
)

    return render(request, "doctor_dashboard.html", {
        "doctor": doctor,
        "scheduled_patients": scheduled_patients
    })
def doctor_home(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = Doctors.objects.get(id=doctor_id)
    return render(request, "doctor_home.html", {"doctor": doctor})
def doctor_database(request):
    query = request.GET.get("q")  # for searching/filtering
    if query:
        doctors = Doctors.objects.filter(
            name__icontains=query
        ) | Doctors.objects.filter(
            email__icontains=query
        ) | Doctors.objects.filter(
            department__icontains=query
        )
    else:
        doctors = Doctors.objects.all()

    return render(request, "doctor_database.html", {"doctors": doctors})
@require_POST
def CompleteReview(request, patient_id):
        doctor_id = request.session.get('doctor_id')
        if not doctor_id:
            messages.error(request, "You are not authorized.")
            return redirect('DoctorsLogin')

        try:
            patient = Patient.objects.get(id=patient_id, doctor_id=doctor_id)
            patient.status = 'reviewed'
            patient.save()
            messages.success(request, f"Patient {patient.name} marked as reviewed.")
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found or unauthorized.")

        return redirect('CompletedReview')


@login_required
def doctor_dashboard(request):
    doctor = Doctors.objects.get(user=request.user)
    allocated_patients = doctor.booking.filter(adminapproval__Approve=True)  # adjust to your model names
    return render(request, "doctor_dashboard.html", {"patients": allocated_patients})
    
def Register_doctor(request):
        if request.method == 'POST':
            #   doctor_id = request.POST.get('doctor_id')
            Name = request.POST.get('Name')
            Email = request.POST.get('Email')
            password = request.POST.get('Password')
            confirm_password = request.POST.get('confirm_password')
            doctor_type = request.POST.get('DoctorType')
            phone = request.POST.get('phone')
            Department = request.POST.get('Department')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'Doctors.registration.html')

            if Doctors.objects.filter(email=Email).exists():
                messages.error(request, "A doctor with this email already exists.")
                return render(request, 'Doctors.registration.html')

            doctor = Doctors.objects.create(
                Name=Name,
                Email=Email,
                password=password,  # Consider hashing this or using Django's auth system
                doctor_type=doctor_type,
                phone=phone,
                department = Department,
                
            )
            
            doctor.save()
            print("Doctor saved:", doctor.id)

            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_database')  # change this to your actual login route name

        return render(request, 'Doctors.registration.html')

def DoctorAuth(request):
        if request.method == 'POST':
            if 'register' in request.POST:
                # Registration logic
                name = request.POST.get('Name')
                email = request.POST.get('Email')
                phone = request.POST.get('phone')
                doctor_type = request.POST.get('doctor_type')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                Department = request.POST.get('Department')
            
                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('DoctorAuth')

                if Doctors.objects.filter(Email=email).exists():
                    messages.error(request, "A doctor with this email already exists.")
                    return redirect('DoctorAuth')

                doctor = Doctors.objects.create(
                    Name=name,
                    Email=email,
                    password=password,
                    doctor_type=doctor_type,
                    phone=phone,
                    status='available'
                )
                doctor.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('DoctorAuth')

            elif 'login' in request.POST:
                # Login logic
                email = request.POST.get('email')
                password = request.POST.get('Password')

                try:
                    doctor = Doctors.objects.get(Email=email)
                    if doctor.password == password:
                        request.session['doctor_id'] = doctor.id
                        messages.success(request, f"Welcome Dr. {doctor.Name}")
                        return redirect('DoctorDashboard')
                    else:
                        messages.error(request, "Incorrect password.")
                except Doctors.DoesNotExist:
                    messages.error(request, "No doctor found with that email.")

        return render(request, 'doctor_auth.html')
def doctors_registration(request):
        if request.method == 'POST':
            doctor_id = request.POST.get('doctor_id')
            password = request.POST.get('password')
            # Here you would typically save the doctor details to the database
            # For now, we will just return a success message
            return HttpResponse(f"Doctor {doctor_id} registered successfully with password {password}")
        return render(request, 'Doctors.registration.html')
def DoctorsPatientRecords(request):
        return render(request,'PatientRecords.html')
def Main_Doctors(request):
        doctors = Doctors.objects.all()
        return render(request, 'doctors.main.html', {'Doctors': doctors})
@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctors.objects.get(user=request.user)
    except Doctors.DoesNotExist:
        return redirect("doctor_login")

    # Get allocated patients/bookings for this doctor
    bookings = Booking.objects.filter(doctor=doctor, status="approved")

    return render(request, "doctor_dashboard.html", {
        "doctor": doctor,
        "bookings": bookings,
    })
def doctor_database(request):
        doctors = Doctors.objects.all()
        return render(request, 'doctor_database.html', {'doctors': doctors})
def admin_appointments(request):
    bookings = Booking.objects.all().order_by("-created_at")
    return render(request, "admin_appointments.html", {"bookings": bookings})

# Approve an appointment
def approve_appointment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_approved = True
    booking.save()
    messages.success(request, f"Appointment for {booking.patient_name} approved.")
    return redirect("admin_appointments")
def reject_appointment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_approved = False
    booking.save()
    messages.error(request, f"Appointment for {booking.patient_name} rejected.")
    return redirect("admin_appointments")

def book_appointment(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'booking_success.html')
    else:
        form = BookingForm()
    return render(request, 'book_appointment.html', {'form': form})

# Doctor submits availability
def doctor_availability(request):
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'availability_success.html')
    else:
        form = DoctorAvailabilityForm()
    return render(request, 'doctor_availability.html', {'form': form})

# Optional: Confirm booking
def confirm_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.confirmed = True
    booking.status = 'doctor_approved'
    booking.save()
    return redirect('book_appointment')
def doctor_management(request):
    # Handle doctor registration
    if request.method == "POST" and "register_doctor" in request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        department = request.POST.get("department")
        doctor_type = request.POST.get("doctor_type")
        password = request.POST.get("password")

        if Doctors.objects.filter(email=email).exists():
            messages.error(request, "Doctor with this email already exists.")
        else:
            Doctors.objects.create(
                name=name,
                email=email,
                contact=contact,
                department=department,
                doctor_type=doctor_type,
                password=password
            )
            messages.success(request, f"Doctor {name} registered successfully!")

        return redirect("doctor_management")

    # Fetch all doctors, schedules, and appointments
    doctors = Doctors.objects.all()
    schedules = DoctorAvailability.objects.all().order_by("date", "start_time")
    appointments = Booking.objects.all().order_by("appointment_date", "appointment_time")


    return render(request, "Doctor_management.html", {
        "doctors": doctors,
        "schedules": schedules,
        "appointments": appointments,
    })
def admin_patient_dashboard(request):
    # Handle approve/reject actions
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = get_object_or_404(Booking, id=booking_id)

        if action == "approve":
            booking.is_approved = True
            messages.success(request, f"Booking for {booking.patient.name} approved.")
        elif action == "reject":
            booking.is_approved = False
            messages.error(request, f"Booking for {booking.patient.name} rejected.")
        
        booking.save()
        return redirect("admin_patient_dashboard")

    # Show all bookings
    bookings = Booking.objects.select_related("patient", "doctor").all().order_by("-created_at")
    return render(request, "admin_patient_dashboard.html", {"bookings": bookings})
@login_required
def book_appointment(request):
    patient_profile, created = PatientProfile.objects.get_or_create(user=request.user)
    doctors = Doctors.objects.all()  # Fetch all doctors

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.patient = patient_profile
            booking.save()
            return redirect("book_appointment")
    else:
        form = BookingForm()

    # Fetch only this patient’s bookings, latest first
    bookings = Booking.objects.filter(patient=patient_profile).order_by('-appointment_date')

    return render(request, "book_appointments.html", {
        "form": form,
        "doctors": doctors,   # ✅ add doctors here
        "bookings": bookings
    })

@login_required
def admin_appointments(request):
    """View all pending appointments for admin review"""
    appointments = Booking.objects.filter(status="pending")
    return render(request, "admin_appointments.html", {"appointments": appointments})


def is_admin(user):
    return user.is_staff  # you can also check user.is_superuser

@login_required
@user_passes_test(is_admin)
def manage_appointments(request):
    appointments = Booking.objects.all().order_by('-appointment_date')
    return render(request, "booking_appointments.html", {"appointments": appointments})

@login_required
@user_passes_test(is_admin)
def admin_approve(request, booking_id):
    appointment = get_object_or_404(Booking, id=booking_id)
    appointment.status = "approved"
    appointment.save()
    messages.success(request, f"Appointment for {appointment.patient.user.username} approved.")
    return redirect("manage_appointments")

@login_required
@user_passes_test(is_admin)
def admin_reject(request, booking_id):
    appointment = get_object_or_404(Booking, id=booking_id)
    appointment.status = "rejected"
    appointment.save()
    messages.error(request, f"Appointment for {appointment.patient.user.username} rejected.")
    return redirect("manage_appointments")

@login_required
def allocate_doctor(request):
    doctor = Doctors.objects.get(user=request.user)  # assuming Doctors is linked to User
    if request.method == "POST":
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()
            return redirect('doctor_dashboard')  # redirect back to dashboard
    else:
        form = DoctorAvailabilityForm()

    # Show previous allocations
    allocations = DoctorAvailability.objects.filter(doctor=doctor).order_by('-date')

    return render(request, "doctor_dashboard/allocate_doctor.html", {
        'form': form,
        'allocations': allocations
    })
@login_required
def my_appointments(request):
    bookings = Booking.objects.filter(patient=request.user).order_by('-date')
    return render(request, "patient_dashboard/my_appointments.html", {"bookings": bookings})
def approve_booking1(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_approved = True
    booking.save()
    messages.success(request, "Booking approved successfully.")
    return redirect('admin_patient_dashboard')

def reject_booking1(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_approved = False
    booking.save()
    messages.error(request, "Booking rejected.")
    return redirect('admin_patient_dashboard')

@login_required
def doctor_allocated_patients(request):
    doctor_profile = Doctors.objects.get(user=request.user)
    for doctor in Doctors.objects.all():
        try:
            user = User.objects.get(email=doctor.email)
            doctor.user = user
            doctor.save()
            print(f"Linked {doctor} to {user}")
        except User.DoesNotExist:
            print(f"No user found for {doctor.email}")

    # Get approved bookings for this doctor
    bookings = Booking.objects.filter(DoctorName=doctor_profile.Name, is_approved=True)

    return render(request, 'allocated_patients.html', {
        'bookings': bookings
    })
def doctor_allocated(request):
    try:
        # Get the doctor's profile linked to the logged-in user
        doctor_profile = Doctors.objects.get(user=request.user)
        
        # Fetch all approved bookings for this doctor
        bookings = Booking.objects.filter(doctor=doctor_profile, is_approved=True)
        
        if not bookings.exists():
            message = "No approved bookings allocated yet."
        else:
            message = None

    except Doctors.DoesNotExist:
        doctor_profile = None
        bookings = None
        message = "No doctor profile found for this user."

    context = {
        'doctor_profile': doctor_profile,
        'bookings': bookings,
        'message': message
    }
    return render(request, 'doctor_allocated.html', context)

@login_required
def doctor_patients(request):
    try:
        doctor = Doctors.objects.get(user=request.user)
    except Doctors.DoesNotExist:
        return redirect("doctor_login")

    # Fetch only approved bookings for this doctor
    patients = Booking.objects.filter(doctor=doctor, is_approved=True)

    return render(request, "doctor_patients.html", {
        "doctor": doctor,
        "patients": patients,
    })