from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models import Sum, Avg


class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.start_date.year}-{self.end_date.year})"


class Semester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Paper(models.Model):
    subject = models.ForeignKey(Subject, related_name='papers', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.subject.code})"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    subjects = models.ManyToManyField(
        Subject,
        related_name='courses',
        blank=True,
        help_text="Subjects included in this course"
    )

    def __str__(self):
        return f"{self.name} ({self.code})"



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
        blank=True,
        related_name= 'sms_student'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = CloudinaryField('image', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    @property
    def full_name(self):
        """Return the full name of the student"""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.admission_number})"

    class Meta:
        ordering = ['last_name', 'first_name']

    def clean(self):
        if self.semester.academic_year != self.academic_year:
            raise ValidationError("Semester must belong to selected academic year")





class Grade(models.Model):  # Moved ABOVE Mark model
    grade = models.CharField(max_length=2)
    min_mark = models.DecimalField(max_digits=5, decimal_places=2)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.grade} ({self.min_mark}-{self.max_mark})"

    @classmethod
    def get_grade(cls, mark):
        try:
            return cls.objects.get(
                min_mark__lte=mark,
                max_mark__gte=mark
            )
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return cls.objects.filter(
                min_mark__lte=mark,
                max_mark__gte=mark
            ).first()

    class Meta:
        ordering = ['-min_mark']

class Mark(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='marks')
    paper = models.ForeignKey('Paper', on_delete=models.CASCADE, related_name='marks')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.ForeignKey('Grade', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Assign grade before saving
        if not self.grade:  # Only calculate if not already set
            self.grade = Grade.get_grade(self.marks_obtained)
        super().save(*args, **kwargs)

    def clean(self):
        if self.marks_obtained > self.paper.max_mark:
            raise ValidationError("Marks obtained cannot exceed paper maximum")
        if self.marks_obtained < 0:
            raise ValidationError("Marks cannot be negative")


class StudentSubjectGrade(models.Model):
    """Stores calculated grades per subject"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    average = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)

    class Meta:
        unique_together = ('student', 'subject', 'semester')

    def save(self, *args, **kwargs):
        self.grade = Grade.get_grade(self.average)
        super().save(*args, **kwargs)


