from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Student, Teacher, Course, Enrollment, Attendance, StudentFeeAccount,
    FeePayment, Mark, GradingSystem, ReportCard, CoCurricularActivity, StudentActivity
)
from .forms import (
    StudentForm, TeacherForm, CourseForm, EnrollmentForm, AttendanceForm,
    FeePaymentForm, MarkForm, ReportCardForm, CoCurricularActivityForm, StudentActivityForm
)

# Student Views
def student_list(request):
    students = Student.objects.all()
    return render(request, 'sms/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'sms/add_student.html', {'form': form})

# Teacher Views
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'sms/teacher_list.html', {'teachers': teachers})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'sms/add_teacher.html', {'form': form})

# Course Views
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'sms/course_list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'sms/add_course.html', {'form': form})

# Enrollment Views
def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'sms/enrollment_list.html', {'enrollments': enrollments})

def add_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'sms/add_enrollment.html', {'form': form})

# Attendance Views
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'sms/attendance_list.html', {'attendances': attendances})

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'sms/add_attendance.html', {'form': form})

# Fee Management Views
def student_fee_account(request, student_id):
    fee_accounts = StudentFeeAccount.objects.filter(student_id=student_id)
    return render(request, 'sms/student_fee_account.html', {'fee_accounts': fee_accounts})

def pay_fees(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_payment_success')
    else:
        form = FeePaymentForm()
    return render(request, 'sms/pay_fees.html', {'form': form})

def fee_payment_success(request):
    return render(request, 'sms/fee_payment_success.html')

# Marks and Grading Views
def mark_list(request):
    marks = Mark.objects.all()
    return render(request, 'sms/mark_list.html', {'marks': marks})

def add_mark(request):
    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mark_list')
    else:
        form = MarkForm()
    return render(request, 'sms/add_mark.html', {'form': form})

# Report Card Views
def report_card_list(request):
    report_cards = ReportCard.objects.all()
    return render(request, 'sms/report_card_list.html', {'report_cards': report_cards})

def add_report_card(request):
    if request.method == 'POST':
        form = ReportCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_card_list')
    else:
        form = ReportCardForm()
    return render(request, 'sms/add_report_card.html', {'form': form})

# Co-curricular Activities Views
def co_curricular_activity_list(request):
    activities = CoCurricularActivity.objects.all()
    return render(request, 'sms/co_curricular_activity_list.html', {'activities': activities})

def add_co_curricular_activity(request):
    if request.method == 'POST':
        form = CoCurricularActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('co_curricular_activity_list')
    else:
        form = CoCurricularActivityForm()
    return render(request, 'sms/add_co_curricular_activity.html', {'form': form})

def student_activity_list(request):
    student_activities = StudentActivity.objects.all()
    return render(request, 'sms/student_activity_list.html', {'student_activities': student_activities})

def add_student_activity(request):
    if request.method == 'POST':
        form = StudentActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_activity_list')
    else:
        form = StudentActivityForm()
    return render(request, 'sms/add_student_activity.html', {'form': form})