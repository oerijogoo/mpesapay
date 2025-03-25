from django.conf import settings
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

    def get_subject_grades(self, academic_year=None, semester=None):
        """Get grades for all subjects for a specific period"""
        papers = Paper.objects.filter(
            mark_set__student=self,  # Changed from mark__student
            subject__course=self.course
        )

        if academic_year:
            papers = papers.filter(subject__academic_year=academic_year)
        if semester:
            papers = papers.filter(subject__semester=semester)

        return papers.values('subject').annotate(
            total_marks=Sum('mark_set__marks_obtained'),  # Changed from mark__
            average=Avg('mark_set__marks_obtained')
        )

    def save(self, *args, **kwargs):
        if not self.admission_number:
            last_student = Student.objects.order_by('-id').first()
            last_id = last_student.id if last_student else 0
            self.admission_number = f"SCH-{last_id + 1:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"


class Mark(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marks'  # This is critical for the query
    )
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    @property
    def grade(self):
        return Grade.get_grade(self.marks_obtained)


class Grade(models.Model):
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
            ).grade
        except cls.DoesNotExist:
            return 'N/A'
        except cls.MultipleObjectsReturned:
            return cls.objects.filter(
                min_mark__lte=mark,
                max_mark__gte=mark
            ).first().grade


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