# hospital/views.py
from .forms import KioskAppointmentForm
from .forms import DoctorAppointmentForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReceptionistAppointmentForm
from django.contrib.auth.decorators import login_required
from .forms import PatientAppointmentForm
from .models import Patient, Doctor, Ward, Bed, Appointment, Admission
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Branch
from .forms import PatientRegistrationForm  # Create this form (see Step 2)


@login_required
def dashboard(request):
    user = request.user

    # Redirect Patients
    if hasattr(user, 'patient'):
        return redirect('patient_dashboard')

    # Redirect Doctors
    elif hasattr(user, 'doctor'):
        return redirect('doctor_dashboard')

    # Redirect Staff/Admins
    elif user.is_staff:
        return redirect('admin_dashboard')

    # Default redirect (e.g., superusers)
    return redirect('home')

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Create the User
            user = form.save()

            # Create the Patient
            patient = Patient(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                contact_number=form.cleaned_data['contact_number'],
                address=form.cleaned_data['address'],
                branch=form.cleaned_data['branch']
            )
            patient.save()

            # Log the user in
            login(request, user)
            return redirect('home')
    else:
        form = PatientRegistrationForm()
    return render(request, 'hospital/patient_register.html', {'form': form})
def home(request):
    return render(request, 'hospital/home.html')


@login_required
def patient_book_appointment(request):
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = Appointment(
                patient=request.user.patient,
                doctor=form.cleaned_data['doctor'],
                appointment_date=form.cleaned_data['appointment_date'],
                is_inpatient=form.cleaned_data['is_inpatient'],
                booked_by='Patient'
            )
            appointment.save()
            return redirect('home')
    else:
        form = PatientAppointmentForm()
    return render(request, 'hospital/patient_book_appointment.html', {'form': form})



@staff_member_required
def receptionist_book_appointment(request):
    if request.method == 'POST':
        form = ReceptionistAppointmentForm(request.POST)
        if form.is_valid():
            appointment = Appointment(
                patient=form.cleaned_data['patient'],
                doctor=form.cleaned_data['doctor'],
                appointment_date=form.cleaned_data['appointment_date'],
                is_inpatient=form.cleaned_data['is_inpatient'],
                booked_by='Receptionist'
            )
            appointment.save()
            return redirect('home')
    else:
        form = ReceptionistAppointmentForm()
    return render(request, 'hospital/receptionist_book_appointment.html', {'form': form})



@login_required
def doctor_book_appointment(request):
    doctor = request.user.doctor
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()

    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST)
        form.fields['patient'].queryset = patients
        if form.is_valid():
            appointment = Appointment(
                patient=form.cleaned_data['patient'],
                doctor=doctor,
                appointment_date=form.cleaned_data['appointment_date'],
                booked_by='Doctor'
            )
            appointment.save()
            return redirect('home')
    else:
        form = DoctorAppointmentForm()
        form.fields['patient'].queryset = patients
    return render(request, 'hospital/doctor_book_appointment.html', {'form': form})



def kiosk_book_appointment(request):
    if request.method == 'POST':
        form = KioskAppointmentForm(request.POST)
        if form.is_valid():
            patient, created = Patient.objects.get_or_create(
                contact_number=form.cleaned_data['contact_number'],
                defaults={'user': None, 'name': form.cleaned_data['patient_name']}
            )
            appointment = Appointment(
                patient=patient,
                doctor=form.cleaned_data['doctor'],
                appointment_date=form.cleaned_data['appointment_date'],
                booked_by='Kiosk'
            )
            appointment.save()
            return redirect('home')
    else:
        form = KioskAppointmentForm()
    return render(request, 'hospital/kiosk_book_appointment.html', {'form': form})

def book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        appointment_date = request.POST['appointment_date']
        is_inpatient = request.POST.get('is_inpatient', False) == 'on'
        doctor = Doctor.objects.get(id=doctor_id)
        patient = Patient.objects.get(user=request.user)
        Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=appointment_date, is_inpatient=is_inpatient)
        return redirect('home')
    doctors = Doctor.objects.filter(availability=True)
    return render(request, 'hospital/book_appointment.html', {'doctors': doctors})

def admit_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        ward_id = request.POST['ward']
        bed_id = request.POST['bed']
        ailment = request.POST['ailment']
        ward = Ward.objects.get(id=ward_id)
        bed = Bed.objects.get(id=bed_id)
        Admission.objects.create(patient=patient, ward=ward, bed=bed, ailment=ailment)
        return redirect('patient_detail', patient_id=patient.id)
    wards = Ward.objects.filter(branch=patient.branch)
    available_beds = Bed.objects.filter(ward__in=wards, is_occupied=False)
    return render(request, 'hospital/admit_patient.html', {'patient': patient, 'wards': wards, 'beds': available_beds})



@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        return redirect('login')  # Restrict access to patients only
    return render(request, 'hospital/patient_dashboard.html')


@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('login')  # Restrict access to doctors only
    return render(request, 'hospital/doctor_dashboard.html')



@staff_member_required
def admin_dashboard(request):
    return render(request, 'hospital/admin_dashboard.html')