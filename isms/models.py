from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils import timezone
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
        ('STAFF', 'Non-Teaching Staff'),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class SchoolConfig(models.Model):
    name = models.CharField(max_length=200)
    logo = CloudinaryField('image', blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    motto = models.CharField(max_length=200, blank=True, null=True)
    student_id_prefix = models.CharField(max_length=10, default='STD')
    teacher_id_prefix = models.CharField(max_length=10, default='TCH')
    staff_id_prefix = models.CharField(max_length=10, default='STF')
    current_academic_year = models.ForeignKey('AcademicYear', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School Configuration"
        verbose_name_plural = "School Configurations"


class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one academic year is marked as current
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date']


class Semester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

    def save(self, *args, **kwargs):
        if self.is_current:
            # Ensure only one semester is marked as current
            Semester.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['start_date']


class ClassLevel(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "Class Level"
        verbose_name_plural = "Class Levels"


class Class(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField(default=30)
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.class_level.name} - {self.name}"

    class Meta:
        verbose_name_plural = "Classes"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    class_levels = models.ManyToManyField(ClassLevel)
    is_core = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_total_weight(self):
        return self.paper_set.aggregate(total=Sum('weight'))['total'] or 0


class Paper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight as percentage of total subject mark"
    )

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

    class Meta:
        unique_together = ('subject', 'code')


class GradingSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            # Ensure only one grading system is marked as default
            GradingSystem.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class Grade(models.Model):
    grading_system = models.ForeignKey(GradingSystem, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    min_score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    points = models.DecimalField(max_digits=3, decimal_places=1)
    remark = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.min_score}-{self.max_score})"

    class Meta:
        ordering = ['-min_score']


class SubjectGrading(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grading_system = models.ForeignKey(GradingSystem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.grading_system}"

    class Meta:
        unique_together = ('subject', 'grading_system')


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    admission_date = models.DateField()
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='YourCountry')
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    def save(self, *args, **kwargs):
        if not self.student_id:
            school_config = SchoolConfig.objects.first()
            if school_config:
                last_student = Student.objects.order_by('-id').first()
                last_id = last_student.id if last_student else 0
                self.student_id = f"{school_config.student_id_prefix}{str(last_id + 1).zfill(4)}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('isms:student_detail', args=[str(self.id)])


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='YourCountry')
    students = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField()
    subjects = models.ManyToManyField(Subject)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            school_config = SchoolConfig.objects.first()
            if school_config:
                last_teacher = Teacher.objects.order_by('-id').first()
                last_id = last_teacher.id if last_teacher else 0
                self.teacher_id = f"{school_config.teacher_id_prefix}{str(last_id + 1).zfill(4)}"
        super().save(*args, **kwargs)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            school_config = SchoolConfig.objects.first()
            if school_config:
                last_staff = Staff.objects.order_by('-id').first()
                last_id = last_staff.id if last_staff else 0
                self.staff_id = f"{school_config.staff_id_prefix}{str(last_id + 1).zfill(4)}"
        super().save(*args, **kwargs)


class ClassSubject(models.Model):
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_info} - {self.subject}"

    class Meta:
        unique_together = ('class_info', 'subject', 'academic_year')


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=(
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('H', 'Half Day'),
    ))
    remark = models.CharField(max_length=100, blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"

    class Meta:
        unique_together = ('student', 'date')


class ExamType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight as percentage of total mark"
    )

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"

    class Meta:
        unique_together = ('exam', 'student', 'subject', 'paper')


class FeeType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choices=(
        ('ONCE', 'One Time'),
        ('MONTHLY', 'Monthly'),
        ('TERMLY', 'Termly'),
        ('YEARLY', 'Yearly'),
    ), default='YEARLY')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FeeStructure(models.Model):
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fee_type} - {self.class_level} - {self.academic_year}"

    class Meta:
        unique_together = ('fee_type', 'class_level', 'academic_year')


class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=(
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('BANK', 'Bank Transfer'),
        ('MOBILE', 'Mobile Money'),
        ('OTHER', 'Other'),
    ))
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.fee_structure} - {self.amount_paid}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"RCPT{str(uuid.uuid4().int)[:10]}"
        super().save(*args, **kwargs)


class Promotion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='promotions_from')
    to_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='promotions_to')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    date = models.DateField()
    promoted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} from {self.from_class} to {self.to_class}"

    class Meta:
        unique_together = ('student', 'academic_year')


class Timetable(models.Model):
    DAY_CHOICES = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )

    class_info = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.class_info} - {self.subject} - {self.day} {self.start_time}-{self.end_time}"

    class Meta:
        ordering = ['day', 'start_time']


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=20, choices=(
        ('ALL', 'All'),
        ('STUDENTS', 'Students'),
        ('TEACHERS', 'Teachers'),
        ('STAFF', 'Staff'),
        ('PARENTS', 'Parents'),
    ), default='ALL')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    audience = models.CharField(max_length=20, choices=(
        ('ALL', 'All'),
        ('STUDENTS', 'Students'),
        ('TEACHERS', 'Teachers'),
        ('STAFF', 'Staff'),
        ('PARENTS', 'Parents'),
    ), default='ALL')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_date']


class LibraryBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    edition = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    cover_image = CloudinaryField('image', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=(
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
        ('LOST', 'Lost'),
    ), default='ISSUED')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_books')

    def __str__(self):
        return f"{self.book} - {self.issued_to}"

    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status == 'ISSUED'

    def save(self, *args, **kwargs):
        if self.is_overdue():
            self.status = 'OVERDUE'
        super().save(*args, **kwargs)