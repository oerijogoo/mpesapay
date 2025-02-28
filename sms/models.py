from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.code} - {self.name}"




class Grading(models.Model):
    GRADE_CHOICES = [
        ('F', 'Fail'),
        ('P', 'Pass'),
        ('D', 'Distinction'),
    ]
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, unique=True)
    min_score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_grade_display()} ({self.min_score}-{self.max_score})"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    enrolled_subjects = models.ManyToManyField(Subject, blank=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.admission_number} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=Student)
def auto_enroll_subjects(sender, instance, created, **kwargs):
    if created and instance.course:
        instance.enrolled_subjects.set(instance.course.subjects.all())


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    date_recorded = models.DateField(auto_now_add=True)


    class Meta:
        unique_together = ('student', 'subject')

    def grade(self):
        if self.score >= 70:
            return 'Distinction'
        elif self.score >= 50:
            return 'Pass'
        return 'Fail'

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.score})"


@receiver(post_save, sender=Student)
def auto_enroll_subjects(sender, instance, created, **kwargs):
    if created and instance.course:
        instance.enrolled_subjects.set(instance.course.subjects.all())