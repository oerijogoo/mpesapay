# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from cloudinary.models import CloudinaryField


class School(models.Model):
    name = models.CharField(max_length=200)
    motto = models.CharField(max_length=200, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = CloudinaryField('logo', folder='isms/school_logos', blank=True)
    established_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one academic year is marked as current
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']
        unique_together = ('academic_year', 'name')

    def __str__(self):
        return f"{self.academic_year} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one semester is marked as current
        if self.is_current:
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    duration_years = models.PositiveIntegerField(default=3)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    courses = models.ManyToManyField(Course, related_name='subjects')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def total_max_weight(self):
        return sum(paper.max_weight for paper in self.papers.all())


class Paper(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='papers')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    max_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage weight of this paper in the subject"
    )
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('subject', 'code')

    def __str__(self):
        return f"{self.subject.code}{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ensure total weight doesn't exceed 100%
        if self.subject.total_max_weight() > 100:
            raise ValueError("Total weight of all papers in a subject cannot exceed 100%")


class GradeScale(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    scale = models.ForeignKey(GradeScale, on_delete=models.CASCADE, related_name='grades')
    name = models.CharField(max_length=10)
    min_mark = models.DecimalField(max_digits=5, decimal_places=2)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)
    points = models.DecimalField(max_digits=3, decimal_places=1)
    remark = models.CharField(max_length=50)

    class Meta:
        ordering = ['-min_mark']
        unique_together = ('scale', 'name')

    def __str__(self):
        return f"{self.name} ({self.min_mark}-{self.max_mark})"


class SubjectGradeScale(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name='grade_scale')
    grade_scale = models.ForeignKey(GradeScale, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.grade_scale}"


class ClassLevel(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    next_level = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_final_level = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Classes"
        unique_together = ('name', 'academic_year')

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='student')
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    photo = CloudinaryField('photo', folder='isms/student_photos', blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    admission_date = models.DateField()
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.admission_number} - {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()


class Staff(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='staff')
    staff_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    photo = CloudinaryField('photo', folder='isms/staff_photos', blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    is_teaching_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.staff_id} - {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()


class ClassSubject(models.Model):
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('class_info', 'subject', 'semester')

    def __str__(self):
        return f"{self.class_info} - {self.subject} - {self.semester}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_info = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrollment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'class_info')

    def __str__(self):
        return f"{self.student} - {self.class_info}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    remarks = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('student', 'class_subject', 'date')

    def __str__(self):
        return f"{self.student} - {self.class_subject} - {self.date} - {self.get_status_display()}"


class ExamType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weight_in_final = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage weight of this exam in the final grade"
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
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.academic_year} - {self.semester}"


class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True, blank=True)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)
    max_marks = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.exam} - {self.class_subject} - {self.paper if self.paper else ''}"


class ExamResult(models.Model):
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('exam_schedule', 'student')

    def __str__(self):
        return f"{self.exam_schedule} - {self.student} - {self.marks_obtained}"

    def percentage(self):
        return (self.marks_obtained / self.exam_schedule.max_marks) * 100


class SubjectResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    average = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('student', 'class_subject', 'exam')

    def __str__(self):
        return f"{self.student} - {self.class_subject} - {self.exam} - {self.average}"


class Promotion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='promotions_from')
    to_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='promotions_to')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    promotion_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.from_class} to {self.to_class}"


class ReportComment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('G', 'General'),
        ('C', 'Class Teacher'),
        ('H', 'Head Teacher'),
    ]

    class_info = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    comment_type = models.CharField(max_length=1, choices=COMMENT_TYPE_CHOICES)
    comment = models.TextField()
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.get_comment_type_display()} - {self.semester}"


class Notification(models.Model):
    recipient = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} - {self.title}"


