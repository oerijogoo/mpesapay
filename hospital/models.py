from django.conf import settings
# hospital/models.py
from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='patients')

    def __str__(self):
        return self.user.get_full_name()

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)  # Doctor's profession (e.g., Cardiologist, Surgeon)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    availability = models.BooleanField(default=True)
    branches = models.ManyToManyField(Branch, related_name='doctors')  # A doctor can work in multiple branches

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.profession})"

class Ward(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='wards')
    total_beds = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

    @property
    def available_beds(self):
        return self.total_beds - self.beds.filter(is_occupied=True).count()

class Bed(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Bed {self.bed_number} in {self.ward.name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    is_inpatient = models.BooleanField(default=False)
    booked_by = models.CharField(
        max_length=20,
        choices=[
            ('Patient', 'Patient'),
            ('Receptionist', 'Receptionist'),
            ('Doctor', 'Doctor'),
            ('Kiosk', 'Kiosk')
        ],
        default='Patient'
    )
class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    ailment = models.TextField()

    def __str__(self):
        return f"Admission for {self.patient} in {self.ward.name} (Bed {self.bed.bed_number})"

    def save(self, *args, **kwargs):
        if not self.discharge_date:
            self.bed.is_occupied = True
            self.bed.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.bed.is_occupied = False
        self.bed.save()
        super().delete(*args, **kwargs)