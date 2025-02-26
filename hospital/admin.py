from django.contrib import admin
from .models import Branch, Patient, Doctor, Ward, Bed, Appointment, Admission

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_number')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'branch')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession', 'specialization', 'contact_number')
    filter_horizontal = ('branches',)  # Allow selecting multiple branches

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'total_beds', 'available_beds')

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'ward', 'is_occupied')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'is_inpatient')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'ward', 'bed', 'admission_date', 'discharge_date')