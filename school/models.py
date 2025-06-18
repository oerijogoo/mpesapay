from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Term(models.Model):
    TERM_CHOICES = [
        (1, 'First Term'),
        (2, 'Second Term'),
        (3, 'Third Term'),
    ]

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.PositiveSmallIntegerField(choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('academic_year', 'term')

    def __str__(self):
        return f"{self.get_term_display()} - {self.academic_year.name}"

class SchoolConfig(models.Model):
    school_name = models.CharField(max_length=200)
    school_logo = CloudinaryField('logo', blank=True, null=True)
    motto = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    student_prefix = models.CharField(max_length=10, default='STD', help_text='Prefix for student registration numbers')
    current_academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True, blank=True)
    current_term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, blank=True)

    # Singleton pattern implementation
    def save(self, *args, **kwargs):
        self.pk = 1  # Force single instance
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.school_name

    class Meta:
        verbose_name = "School Configuration"
        verbose_name_plural = "School Configurations"

class ClassLevel(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    next_class = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    is_core = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class SubSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    class Meta:
        unique_together = ('subject', 'code')

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class ClassSubject(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_compulsory = models.BooleanField(default=True)

    class Meta:
        unique_together = ('class_level', 'subject')

    def __str__(self):
        return f"{self.class_level.name} - {self.subject.name}"


class GradingSystem(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade_name = models.CharField(max_length=10)
    min_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    points = models.DecimalField(max_digits=3, decimal_places=1)
    remark = models.CharField(max_length=50)

    class Meta:
        unique_together = ('subject', 'grade_name')
        ordering = ['subject', '-min_score']

    def __str__(self):
        return f"{self.subject.name} - {self.grade_name}"


class Staff(models.Model):
    STAFF_TYPE = [
        ('TEACHING', 'Teaching Staff'),
        ('NON-TEACHING', 'Non-Teaching Staff'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=STAFF_TYPE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    photo = CloudinaryField('photo', blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"


class Teacher(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    class_teacher_of = models.ForeignKey(ClassLevel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.staff.user.get_full_name()


class Parent(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    occupation = models.CharField(max_length=100, blank=True)
    photo = CloudinaryField('photo', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    current_class = models.ForeignKey(ClassLevel, on_delete=models.SET_NULL, null=True)
    parents = models.ManyToManyField(Parent, blank=True)
    admission_date = models.DateField(auto_now_add=True)
    photo = CloudinaryField('photo', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"


class ExamType(models.Model):
    name = models.CharField(max_length=100)
    weight = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.term}"


class StudentMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2,
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.CharField(max_length=10, blank=True)
    points = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    remark = models.CharField(max_length=50, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'exam', 'subject')

    def save(self, *args, **kwargs):
        # Auto-calculate grade and points based on grading system
        grading = GradingSystem.objects.filter(
            subject=self.subject,
            min_score__lte=self.marks,
            max_score__gte=self.marks
        ).first()

        if grading:
            self.grade = grading.grade_name
            self.points = grading.points
            self.remark = grading.remark

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"


class FeeStructure(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('class_level', 'term')

    def __str__(self):
        return f"{self.class_level} - {self.term} - KES {self.amount}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MPESA', 'M-Pesa'),
        ('BANK', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.receipt_number}"