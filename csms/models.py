import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from cloudinary.models import CloudinaryField


class SchoolSettings(models.Model):
    name = models.CharField(max_length=200)
    logo = CloudinaryField(
        'image',
        folder='school/logo/',
        transformation={'quality': 'auto:best'},
        null=True,
        blank=True
    )
    motto = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    admission_number_prefix = models.CharField(max_length=10, default='STD')
    current_academic_year = models.ForeignKey('AcademicYear', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "School Setting"
        verbose_name_plural = "School Settings"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if SchoolSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one school setting can be created")
        super().save(*args, **kwargs)


class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Years"

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")

    def save(self, *args, **kwargs):
        # Ensure only one academic year is marked as current
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(models.Model):
    name = models.CharField(max_length=50)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < self.academic_year.start_date or self.end_date > self.academic_year.end_date:
            raise ValidationError("Semester dates must be within academic year dates")

    def save(self, *args, **kwargs):
        # Ensure only one semester is marked as current
        if self.is_current:
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class AcademicLevel(models.Model):
    LEVEL_CHOICES = [
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Degree', 'Degree'),
        ('Masters', 'Masters'),
        ('PhD', 'PhD'),
    ]

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in years")  # Duration in years
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['level', 'name']
        verbose_name = "Academic Level"
        verbose_name_plural = "Academic Levels"

    def __str__(self):
        return f"{self.level} - {self.name}"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.PROTECT)
    duration = models.PositiveIntegerField(help_text="Duration in semesters")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['academic_level', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse('subject_detail', kwargs={'pk': self.pk})


class Paper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='papers')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight as percentage (total for all papers in subject should be 100)"
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['subject', 'code']
        unique_together = ['subject', 'code']

    def __str__(self):
        return f"{self.subject.code} - {self.code}: {self.name}"

    def clean(self):
        # Check that the sum of weights for all papers in the subject doesn't exceed 100
        if self.pk:  # If updating existing paper
            other_papers = Paper.objects.filter(subject=self.subject).exclude(pk=self.pk)
        else:  # If creating new paper
            other_papers = Paper.objects.filter(subject=self.subject)

        total_weight = sum(p.weight for p in other_papers) + self.weight
        if total_weight > 100:
            raise ValidationError(
                f"Total weight for all papers in this subject would be {total_weight}%. It must not exceed 100%.")


class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_core = models.BooleanField(default=True)
    credits = models.PositiveIntegerField(default=3)

    class Meta:
        ordering = ['course', 'semester', 'subject']
        unique_together = ['course', 'subject', 'semester']
        verbose_name = "Course Subject"
        verbose_name_plural = "Course Subjects"

    def __str__(self):
        return f"{self.course} - {self.subject} - {self.semester}"

    def get_absolute_url(self):
        return reverse('course_subject_detail', kwargs={'pk': self.pk})


class GradingScale(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Grading Scale"
        verbose_name_plural = "Grading Scales"

    def __str__(self):
        return self.name


class Grade(models.Model):
    grading_scale = models.ForeignKey(GradingScale, on_delete=models.CASCADE, related_name='grades')
    name = models.CharField(max_length=20)
    min_score = models.DecimalField(max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_score = models.DecimalField(max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    points = models.DecimalField(max_digits=3, decimal_places=1)
    remark = models.CharField(max_length=100)

    class Meta:
        ordering = ['grading_scale', '-points']
        unique_together = ['grading_scale', 'name']

    def __str__(self):
        return f"{self.grading_scale}: {self.name} ({self.min_score}-{self.max_score})"

    def clean(self):
        if self.min_score >= self.max_score:
            raise ValidationError("Min score must be less than max score")

        # Check for overlapping ranges within the same grading scale
        overlapping_grades = Grade.objects.filter(
            grading_scale=self.grading_scale,
            min_score__lt=self.max_score,
            max_score__gt=self.min_score
        ).exclude(pk=self.pk)

        if overlapping_grades.exists():
            raise ValidationError("This grade range overlaps with existing grades in the same grading scale")


class SubjectGrading(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grading_schemes')
    grading_scale = models.ForeignKey(GradingScale, on_delete=models.PROTECT)
    number_of_papers = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Subject Grading"
        verbose_name_plural = "Subject Gradings"
        unique_together = ['subject', 'number_of_papers']

    def __str__(self):
        return f"{self.subject} - {self.grading_scale} ({self.number_of_papers} papers)"


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    staff_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    photo = CloudinaryField(
        'image',
        folder='teachers/photos/',
        transformation={'quality': 'auto:good', 'width': 300, 'height': 300, 'crop': 'thumb', 'gravity': 'face'},
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"

    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'pk': self.pk})


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    admission_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    photo = CloudinaryField(
        'image',
        folder='students/photos/',
        transformation={'quality': 'auto:good', 'width': 300, 'height': 300, 'crop': 'thumb', 'gravity': 'face'},
        blank=True,
        null=True
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

    def save(self, *args, **kwargs):
        if not self.admission_number:
            # Generate admission number if not provided
            school_settings = SchoolSettings.objects.first()
            prefix = school_settings.admission_number_prefix if school_settings else 'STD'
            last_student = Student.objects.order_by('-id').first()
            last_id = last_student.id if last_student else 0
            self.admission_number = f"{prefix}{str(last_id + 1).zfill(5)}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    enrollment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['student', 'semester']

    def __str__(self):
        return f"{self.student} - {self.course} - {self.semester}"

    def clean(self):
        # Check if student is already enrolled in this semester
        if Enrollment.objects.filter(student=self.student, semester=self.semester).exclude(pk=self.pk).exists():
            raise ValidationError("Student is already enrolled in this semester")


class Class(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='classes')
    subjects = models.ManyToManyField(Subject, through='ClassSubject')

    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['academic_year', 'semester', 'course', 'name']
        unique_together = ['name', 'academic_year', 'semester']

    def __str__(self):
        return f"{self.name} - {self.course} - {self.semester}"

    def get_absolute_url(self):
        return reverse('class_detail', kwargs={'pk': self.pk})


class ClassSubject(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Class Subject"
        verbose_name_plural = "Class Subjects"
        unique_together = ['class_obj', 'subject']

    def __str__(self):
        return f"{self.class_obj} - {self.subject}"


class ExamType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight as percentage of total marks"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=200)
    exam_type = models.ForeignKey(ExamType, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.semester}"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < self.semester.start_date or self.end_date > self.semester.end_date:
            raise ValidationError("Exam dates must be within semester dates")

    def get_absolute_url(self):
        return reverse('exam_detail', kwargs={'pk': self.pk})


class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)

    class Meta:
        ordering = ['exam', 'date', 'start_time']
        unique_together = ['exam', 'subject']

    def __str__(self):
        return f"{self.exam} - {self.subject} - {self.date}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        if self.date < self.exam.start_date or self.date > self.exam.end_date:
            raise ValidationError("Exam schedule date must be within exam dates")


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    paper = models.ForeignKey(Paper, on_delete=models.PROTECT, null=True, blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    comment = models.CharField(max_length=100, blank=True)
    entered_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['exam', 'subject', 'student']
        unique_together = ['student', 'exam', 'subject', 'paper']

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.subject}: {self.marks}"

    def clean(self):
        if self.paper and self.paper.subject != self.subject:
            raise ValidationError("Paper must belong to the selected subject")


class GradeAllocation(models.Model):
    mark = models.OneToOneField(Mark, on_delete=models.CASCADE, related_name='grade')
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    points = models.DecimalField(max_digits=3, decimal_places=1)
    remark = models.CharField(max_length=100)
    allocated_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-allocated_at']

    def __str__(self):
        return f"{self.mark}: {self.grade.name}"


class AcademicReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT)
    overall_grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    average_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_points = models.DecimalField(max_digits=5, decimal_places=2)
    position = models.PositiveIntegerField()
    remarks = models.TextField()
    generated_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-exam', 'position']
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"{self.student} - {self.exam}: Position {self.position}"


class FeeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    fee_type = models.ForeignKey(FeeType, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['academic_year', 'course', 'fee_type']
        unique_together = ['course', 'academic_year', 'fee_type']

    def __str__(self):
        return f"{self.course} - {self.fee_type}: {self.amount}"


class StudentFee(models.Model):
    PAYMENT_STATUS = [
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('unpaid', 'Unpaid'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.PROTECT)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    transaction_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)
    received_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student} - {self.fee_structure}: {self.amount_paid}"

    def clean(self):
        if self.amount_paid > self.fee_structure.amount:
            raise ValidationError("Amount paid cannot be more than the fee amount")

        if self.amount_paid == self.fee_structure.amount:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'


class AcademicCalendar(models.Model):
    EVENT_TYPE_CHOICES = [
        ('holiday', 'Holiday'),
        ('exam', 'Examination'),
        ('event', 'School Event'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")
        if self.start_date < self.academic_year.start_date or self.end_date > self.academic_year.end_date:
            raise ValidationError("Event dates must be within academic year dates")


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.CharField(max_length=100, blank=True)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student} - {self.date}: {self.status}"

    def clean(self):
        # Check if date is within academic year
        academic_year = AcademicYear.objects.filter(
            start_date__lte=self.date,
            end_date__gte=self.date
        ).first()

        if not academic_year:
            raise ValidationError("Attendance date must be within an academic year")


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('fee', 'Fee'),
        ('exam', 'Exam'),
        ('event', 'Event'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title