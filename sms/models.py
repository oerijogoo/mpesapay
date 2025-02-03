from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    guardian_name = models.CharField(max_length=150)
    guardian_contact = models.CharField(max_length=15)
    address = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.admission_number}"


@receiver(pre_save, sender=Student)
def generate_admission_number(sender, instance, **kwargs):
    if not instance.admission_number:  # Only generate if it's not already set
        current_year = datetime.now().year
        school_initial = "M"  # Replace with your school's initial
        last_student = Student.objects.filter(admission_number__startswith=f"{school_initial}{current_year}_").order_by(
            'id').last()

        if last_student:
            # Extract the last number and increment it
            last_number = int(last_student.admission_number.split("_")[-1])
            new_number = last_number + 1
        else:
            # Start from 1 if no students exist for the current year
            new_number = 1

        # Format the new admission number
        instance.admission_number = f"{school_initial}{current_year}_{new_number:02d}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    subjects = models.ManyToManyField('Subject', related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Classroom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classrooms')
    students = models.ManyToManyField(Student, related_name='classrooms')

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.CharField(max_length=20)
    year = models.IntegerField()
    marks = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('student', 'subject', 'term', 'year')

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.term} {self.year})"



class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
