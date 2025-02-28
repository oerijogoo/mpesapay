from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credit_hours = models.PositiveIntegerField(default=3)  # Added credit hours

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    subjects = models.ManyToManyField(Subject)
    duration_years = models.PositiveIntegerField(default=4)  # Course duration

    def __str__(self):
        return f"{self.code} - {self.name}"


class Grading(models.Model):
    GRADE_CHOICES = [
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Average'),
        ('D', 'Below Average'),
        ('F', 'Fail'),
    ]
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    min_score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-min_score']

    def clean(self):
        if self.min_score >= self.max_score:
            raise ValidationError("Min score must be less than max score")

    def __str__(self):
        return f"{self.get_grade_display()} ({self.min_score}-{self.max_score})"


class Student(models.Model):
    YEAR_CHOICES = [(i, f'Year {i}') for i in range(1, 5)]
    SEMESTER_CHOICES = [(1, 'Semester 1'), (2, 'Semester 2')]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    enrolled_subjects = models.ManyToManyField(Subject, blank=True)
    year_of_study = models.PositiveIntegerField(choices=YEAR_CHOICES, default=1)
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES, default=1)
    enrollment_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.admission_number} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def average_score(self):
        marks = self.mark_set.all()
        if marks.exists():
            return round(sum(mark.score for mark in marks) / marks.count(), 2)
        return 0

    @property
    def overall_grade(self):
        try:
            return Grading.objects.filter(
                min_score__lte=self.average_score,
                max_score__gte=self.average_score
            ).first().grade
        except AttributeError:
            return 'Ungraded'

    @property
    def credit_points(self):
        return sum(
            mark.subject.credit_hours * (mark.score / 100)
            for mark in self.mark_set.all()
        )


@receiver(post_save, sender=Student)
def auto_enroll_subjects(sender, instance, created, **kwargs):
    if created and instance.course:
        instance.enrolled_subjects.set(instance.course.subjects.all())


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    date_recorded = models.DateField(auto_now_add=True)
    is_absent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'subject')
        ordering = ['-date_recorded']

    def clean(self):
        if self.score > 100:
            raise ValidationError("Score cannot exceed 100")

    @property
    def grade(self):
        if self.is_absent:
            return 'Absent'
        try:
            return Grading.objects.filter(
                min_score__lte=self.score,
                max_score__gte=self.score
            ).first().grade
        except AttributeError:
            return 'Ungraded'

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.score})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'date', 'subject')
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"


class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=9)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def total_fee(self):
        return sum([
            self.tuition_fee,
            self.registration_fee,
            self.examination_fee
        ])

    def __str__(self):
        return f"{self.course} Fee Structure {self.academic_year}"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    receipt_number = models.CharField(max_length=20, unique=True)
    payment_method = models.CharField(max_length=50, default='MPesa')
    verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.payment_date})"