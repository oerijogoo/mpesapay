from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField


class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()


class Semester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)


class Paper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    subjects = models.ManyToManyField(Subject)


class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = CloudinaryField('image', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            last_student = Student.objects.order_by('-id').first()
            last_id = last_student.id if last_student else 0
            self.admission_number = f"SCH-{last_id + 1:03d}"
        super().save(*args, **kwargs)


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)


class Grade(models.Model):
    grade = models.CharField(max_length=2)
    min_mark = models.DecimalField(max_digits=5, decimal_places=2)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)