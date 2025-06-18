from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


# ==================== Authentication Views ====================


def user_login(request):
    next_url = request.GET.get('next', request.POST.get('next', 'dashboard'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Safely redirect to `next_url` only if it's a trusted host
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('school:dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'school/auth/login.html', {'next': next_url})



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'school/auth/password_change.html', {'form': form})


# ==================== Dashboard ====================
@login_required
def dashboard(request):
    school = SchoolConfig.objects.first()
    stats = {
        'students': Student.objects.count(),
        'staff': Staff.objects.count(),
        'parents': Parent.objects.count(),
        'classes': ClassLevel.objects.count(),
    }
    return render(request, 'school/dashboard.html', {'school': school, 'stats': stats})


# ==================== School Configuration ====================
@login_required
def school_config_view(request):
    # Get or create school config
    school, created = SchoolConfig.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = SchoolConfigForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, 'School configuration updated successfully')
            return redirect('school:school_config')
    else:
        form = SchoolConfigForm(instance=school)

    return render(request, 'school/config/school_config.html', {
        'form': form,
        'school': school
    })


# ==================== Academic Structure Views ====================
@login_required
def academic_year_list(request):
    years = AcademicYear.objects.all().order_by('-start_date')
    return render(request, 'school/academics/year_list.html', {'years': years})


@login_required
def academic_year_add(request):
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic year added successfully')
            return redirect('school:academic_years')
    else:
        form = AcademicYearForm()
    return render(request, 'school/academics/year_form.html', {'form': form})


@login_required
def academic_year_edit(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        form = AcademicYearForm(request.POST, instance=year)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic year updated successfully')
            return redirect('school:academic_years')
    else:
        form = AcademicYearForm(instance=year)
    return render(request, 'school/academics/year_form.html', {'form': form})


# Similar views for Term (term_list, term_add, term_edit)
@login_required
def term_list(request):
    terms = Term.objects.all().order_by('-academic_year', 'term')
    return render(request, 'school/academics/term_list.html', {'terms': terms})


@login_required
def term_add(request):
    academic_year = request.GET.get('year')
    initial = {}

    if academic_year:
        initial = {'academic_year': academic_year}

    if request.method == 'POST':
        form = TermForm(request.POST, initial=initial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Term added successfully')
            return redirect('school:terms')
    else:
        form = TermForm(initial=initial)

    return render(request, 'school/academics/term_form.html', {
        'form': form,
        'academic_year': academic_year
    })


@login_required
def term_edit(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, 'Term updated successfully')
            return redirect('school:terms')
    else:
        form = TermForm(instance=term)
    return render(request, 'school/academics/term_form.html', {'form': form})


# ==================== Class Management Views ====================
@login_required
def class_list(request):
    classes = ClassLevel.objects.all().order_by('name')
    return render(request, 'school/classes/class_list.html', {'classes': classes})


@login_required
def class_add(request):
    if request.method == 'POST':
        form = ClassLevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class added successfully')
            return redirect('school:classes')
    else:
        form = ClassLevelForm()
    return render(request, 'school/classes/class_form.html', {'form': form})


@login_required
def class_edit(request, pk):
    class_level = get_object_or_404(ClassLevel, pk=pk)
    if request.method == 'POST':
        form = ClassLevelForm(request.POST, instance=class_level)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully')
            return redirect('school:classes')
    else:
        form = ClassLevelForm(instance=class_level)
    return render(request, 'school/classes/class_form.html', {'form': form})


# ==================== Subject Management Views ====================
@login_required
def subject_list(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'school/subjects/subject_list.html', {'subjects': subjects})


@login_required
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully')
            return redirect('subjects')
    else:
        form = SubjectForm()
    return render(request, 'school/subjects/subject_form.html', {'form': form})


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully')
            return redirect('subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'school/subjects/subject_form.html', {'form': form})


# ==================== Staff Management Views ====================
@login_required
def staff_list(request):
    staff = Staff.objects.all().order_by('user__last_name')
    return render(request, 'school/staff/staff_list.html', {'staff': staff})


@login_required
def staff_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST, request.FILES)
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()
            messages.success(request, 'Staff member added successfully')
            return redirect('school/staff_list')
    else:
        user_form = UserForm()
        staff_form = StaffForm()
    return render(request, 'school/staff/staff_form.html', {
        'user_form': user_form,
        'staff_form': staff_form
    })


@login_required
def staff_edit(request, pk):
    staff = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'staff updated successfully')
            return redirect('school:staff')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'school/staff/staff_form.html', {'form': form})

@login_required
def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    return render(request, 'school/staff/staff_detail.html', {'staff': staff})


# ==================== Student Management Views ====================
@login_required
def student_list(request):
    students = Student.objects.all().order_by('user__last_name')
    return render(request, 'school/students/student_list.html', {'students': students})


@login_required
def student_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user

            # Generate admission number
            school_config = SchoolConfig.objects.first()
            if school_config:
                last_student = Student.objects.order_by('-id').first()
                last_id = int(last_student.admission_number[len(school_config.student_prefix):]) if last_student else 0
                student.admission_number = f"{school_config.student_prefix}{last_id + 1:04d}"

            student.save()
            student_form.save_m2m()  # Save many-to-many relationships (parents)
            messages.success(request, 'Student added successfully')
            return redirect('school:students')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request, 'school/students/student_form.html', {
        'user_form': user_form,
        'student_form': student_form
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'school/students/student_detail.html', {'student': student})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'student updated successfully')
            return redirect('school:staff')
    else:
        form = StudentForm(instance=student)
    return render(request, 'school/students/student_form.html', {'form': form})
# ==================== Parent Management Views ====================
@login_required
def parent_list(request):
    parents = Parent.objects.all().order_by('user__last_name')
    return render(request, 'school/parents/parent_list.html', {'parents': parents})


@login_required
def parent_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        parent_form = ParentForm(request.POST, request.FILES)
        if user_form.is_valid() and parent_form.is_valid():
            user = user_form.save()
            parent = parent_form.save(commit=False)
            parent.user = user
            parent.save()
            parent_form.save_m2m()  # Save many-to-many relationships (students)
            messages.success(request, 'Parent added successfully')
            return redirect('school:parents')
    else:
        user_form = UserForm()
        parent_form = ParentForm()
    return render(request, 'school/parents/parent_form.html', {
        'user_form': user_form,
        'parent_form': parent_form
    })


@login_required
def parent_detail(request, pk):
    parent = get_object_or_404(Parent, pk=pk)
    return render(request, 'school/parents/parent_detail.html', {'parent': parent})


@login_required
def parent_edit(request, pk):
    parent = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            messages.success(request, 'parent updated successfully')
            return redirect('school:staff')
    else:
        form = ParentForm(instance=parent)
    return render(request, 'school/parents/parent_form.html', {'form': form})


# ==================== Examination System Views ====================
@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by('-term__academic_year', 'term', 'start_date')
    return render(request, 'school/exams/exam_list.html', {'exams': exams})


@login_required
def exam_add(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully')
            return redirect('school:exams')
    else:
        form = ExamForm()
    return render(request, 'school/exams/exam_form.html', {'form': form})


@login_required
def exam_marks(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    marks = StudentMark.objects.filter(exam=exam).select_related('student', 'subject')
    return render(request, 'school/exams/exam_marks.html', {'exam': exam, 'marks': marks})


# ==================== Finance Views ====================
@login_required
def fee_structure_list(request):
    fee_structures = FeeStructure.objects.all().order_by('-term__academic_year', 'term', 'class_level')
    return render(request, 'school/finance/fee_structure_list.html', {'fee_structures': fee_structures})


@login_required
def fee_structure_add(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure added successfully')
            return redirect('fee_structures')
    else:
        form = FeeStructureForm()
    return render(request, 'school/finance/fee_structure_form.html', {'form': form})


@login_required
def payment_list(request):
    payments = Payment.objects.all().order_by('-transaction_date')
    return render(request, 'school/finance/payment_list.html', {'payments': payments})


@login_required
def payment_add(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment recorded successfully')
            return redirect('school:payments')
    else:
        form = PaymentForm()
    return render(request, 'school/finance/payment_form.html', {'form': form})


# ==================== Report Views ====================
@login_required
def student_reports(request):
    students = Student.objects.all().order_by('current_class', 'user__last_name')
    return render(request, 'school/reports/student_reports.html', {'students': students})


@login_required
def class_reports(request):
    classes = ClassLevel.objects.all().order_by('name')
    return render(request, 'school/reports/class_reports.html', {'classes': classes})


@login_required
def exam_reports(request):
    exams = Exam.objects.all().order_by('-term__academic_year', 'term')
    return render(request, 'school/reports/exam_reports.html', {'exams': exams})


# school/views.py
def test_context(request):
    from django.template import RequestContext
    context = RequestContext(request)  # This will include all context processors
    return JsonResponse({
        'available_data': list(context.flatten().keys()),
        'school_config': str(SchoolConfig.load())
    })