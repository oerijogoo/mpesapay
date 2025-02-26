from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Branch, Doctor

class PatientRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all())

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'gender', 'contact_number', 'address', 'branch')


class PatientAppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.filter(availability=True))
    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    is_inpatient = forms.BooleanField(required=False, label="Inpatient?")


class ReceptionistAppointmentForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all())
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.filter(availability=True))
    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    is_inpatient = forms.BooleanField(required=False, label="Inpatient?")


class DoctorAppointmentForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.none())  # Queryset will be set dynamically in the view
    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))



class KioskAppointmentForm(forms.Form):
    patient_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.filter(availability=True))
    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))