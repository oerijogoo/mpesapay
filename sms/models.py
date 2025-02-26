from django.db import models

class AcademicYear(models.Model):
    year = models.CharField(max_length=9, unique=True)  # e.g., "2023-2024"

    def __str__(self):
        return self.year

class Term(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Term 1", "Term 2", "Term 3"
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Fee for this term

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    admission_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    staff_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class StudentFeeAccount(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total fees for the term
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Amount paid so far
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Remaining balance

    def save(self, *args, **kwargs):
        # Automatically calculate the balance
        self.balance = self.total_fees - self.amount_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.term} - Balance: {self.balance}"

class FeePayment(models.Model):
    student_fee_account = models.ForeignKey(StudentFeeAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update the StudentFeeAccount when a payment is made
        super().save(*args, **kwargs)
        self.student_fee_account.amount_paid += self.amount
        self.student_fee_account.save()

    def __str__(self):
        return f"{self.student_fee_account.student} - {self.amount} - {self.date_paid}"

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.term} - {self.score}"

class GradingSystem(models.Model):
    grade = models.CharField(max_length=2)  # e.g., "A", "B", "C"
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.grade} ({self.min_score} - {self.max_score})"

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    comments = models.TextField()

    def __str__(self):
        return f"{self.student} - {self.term}"

class CoCurricularActivity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class StudentActivity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(CoCurricularActivity, on_delete=models.CASCADE)
    date = models.DateField()
    remarks = models.TextField()

    def __str__(self):
        return f"{self.student} - {self.activity} - {self.date}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status}"