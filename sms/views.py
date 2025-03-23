from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from weasyprint import HTML
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
import csv
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError



def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.all().order_by('-id')

    if query:
        students = students.filter(
            Q(admission_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sms/student_list.html', {'students': page_obj})



def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'sms/student_detail.html', {'student': student})



def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # Create student without user association
            student = form.save(commit=False)
            student.save()
            messages.success(request, 'Student created successfully!')
            return redirect('sms:student_list')
    else:
        form = StudentForm()
    return render(request, 'sms/student_form.html', {'form': form})



def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'sms/student_form.html', {'form': form})



def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'sms/student_confirm_delete.html', {'student': student})



def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    subjects_data = []

    for subject in student.course.subjects.all():
        papers = Paper.objects.filter(subject=subject)
        subject_marks = []

        for paper in papers:
            try:
                mark = Mark.objects.get(student=student, paper=paper)
                subject_marks.append({
                    'paper': paper.name,
                    'marks': mark.marks_obtained,
                    'max': paper.max_mark
                })
            except Mark.DoesNotExist:
                continue

        if subject_marks:
            average = sum(m['marks'] for m in subject_marks) / len(subject_marks)
            subjects_data.append({
                'subject': subject,
                'papers': subject_marks,
                'average': round(average, 2),
                'grade': Grade.get_grade(average)
            })

    context = {
        'student': student,
        'subjects_data': subjects_data,
        'overall_average': round(
            sum(s['average'] for s in subjects_data) / len(subjects_data), 2
        ) if subjects_data else 0
    }
    return render(request, 'sms/report.html', context)



def generate_pdf_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = student_report(request, pk).context_data

    html_string = render_to_string('sms/pdf_report.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=report_{student.admission_number}.pdf'
    return response

# Add similar CRUD views for Course, Subject, AcademicYear, etc.


def course_list(request):
    courses = Course.objects.all().order_by('-id')
    return render(request, 'sms/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'sms/course_detail.html', {'course': course})


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('sms:course_list')  # Changed to course_list
    else:
        form = CourseForm()
    return render(request, 'sms/course_form.html', {'form': form})


def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'sms/course_form.html', {'form': form})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    return render(request, 'sms/course_confirm_delete.html', {'course': course})


@login_required
def subject_list(request):
    subjects = Subject.objects.all().order_by('-id')
    return render(request, 'sms/subject_list.html', {'subjects': subjects})

@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'sms/subject_detail.html', {'subject': subject})


def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('sms:subject_list')  # Changed to subject_list
    else:
        form = SubjectForm()
    return render(request, 'sms/subject_form.html', {'form': form})


def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('subject_detail', pk=pk)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'sms/subject_form.html', {'form': form})


def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subject_list')
    return render(request, 'sms/subject_confirm_delete.html', {'subject': subject})



def academic_year_list(request):
    years = AcademicYear.objects.all().order_by('-start_date')
    return render(request, 'sms/academic_year_list.html', {'years': years})


def academic_year_detail(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    return render(request, 'sms/academic_year_detail.html', {'year': year})


def academic_year_create(request):
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic year created successfully!')
            return redirect('sms:academic_year_list')  # Remove the pk parameter
    else:
        form = AcademicYearForm()
    return render(request, 'sms/academic_year_form.html', {'form': form})


def academic_year_update(request, pk):
    academic_year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        form = AcademicYearForm(request.POST, instance=academic_year)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic year updated successfully!')
            return redirect('academic_year_detail', pk=pk)
    else:
        form = AcademicYearForm(instance=academic_year)
    return render(request, 'sms/academic_year_form.html', {'form': form})


def academic_year_delete(request, pk):
    academic_year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        academic_year.delete()
        messages.success(request, 'Academic year deleted successfully!')
        return redirect('sms:academic_year_list')
    return render(request, 'sms/academic_year_confirm_delete.html', {
        'academic_year': academic_year  # Pass context with correct variable name
    })



def mark_bulk_entry(request):
    def process_mark(data, paper):  # Nested function to fix 'self' reference
        student = Student.objects.get(admission_number=data['admission_number'].strip())
        mark = Decimal(data['marks_obtained'])

        if mark > paper.max_mark:
            raise ValidationError(
                f"Mark {mark} exceeds maximum {paper.max_mark} for {student}"
            )

        Mark.objects.update_or_create(
            student=student,
            paper=paper,
            defaults={'marks_obtained': mark}
        )

    if request.method == 'POST':
        form = BulkMarkForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    paper = form.cleaned_data['paper']
                    entry_type = form.cleaned_data['entry_type']
                    count = 0

                    if entry_type == 'csv':
                        csv_file = request.FILES['csv_file']
                        reader = csv.DictReader(
                            csv_file.read().decode('utf-8').splitlines(),
                            fieldnames=['admission_number', 'marks_obtained']
                        )
                        for row in reader:
                            process_mark(row, paper)  # Fixed: removed 'self.'
                            count += 1

                    elif entry_type == 'manual':
                        for line in form.cleaned_data['marks_data'].split('\n'):
                            adm_no, mark = line.strip().split(',')
                            process_mark(  # Fixed: removed 'self.'
                                {'admission_number': adm_no, 'marks_obtained': mark},
                                paper
                            )
                            count += 1

                    messages.success(request,
                                     f"Added {count} marks for {paper.subject.name} - {paper.name}")
                    return redirect('subject_list')

            except ValidationError as e:
                messages.error(request, f"Validation Error: {e}")
            except Student.DoesNotExist:
                messages.error(request, "Invalid admission number found")
            except ValueError:
                messages.error(request, "Invalid mark format (must be numeric)")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = BulkMarkForm()

    return render(request, 'sms/bulk_mark_entry.html', {'form': form})


def student_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sms:student_profile')
    else:
        form = UserCreationForm()

    # Pass request context explicitly
    return render(request, 'sms/auth/student_signup.html', {'form':form})

def teacher_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teacher_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'sms/auth/teacher_signup.html', {'form': form})



def student_profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'sms/student_profile.html', {'student': student})



def semester_list(request):
    semesters = Semester.objects.all().order_by('-start_date')
    return render(request, 'sms/semester_list.html', {'semesters': semesters})


def semester_detail(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    return render(request, 'sms/semester_detail.html', {'semester': semester})


def semester_create(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save()
            messages.success(request, 'Semester created successfully!')
            return redirect('sms:semester_list')
    else:
        form = SemesterForm()
    return render(request, 'sms/semester_form.html', {'form': form})


def semester_update(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semester updated successfully!')
            return redirect('sms:semester_detail', pk=semester.pk)
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'sms/semester_form.html', {'form': form})


def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        semester.delete()
        messages.success(request, 'Semester deleted successfully!')
        return redirect('sms:semester_list')
    return render(request, 'sms/semester_confirm_delete.html', {'semester': semester})


def load_academic_years(request):
    academic_years = AcademicYear.objects.all().order_by('-start_date')
    return render(request, 'sms/includes/academic_year_options.html',
                 {'academic_years': academic_years})


# sms/views.py
from django.db.models import Avg
from weasyprint import HTML


def student_progressive_report(request, pk):
    student = get_object_or_404(Student, pk=pk)

    # Get all marks grouped by semester
    progress_data = []
    for semester in Semester.objects.filter(academic_year=student.academic_year):
        marks = Mark.objects.filter(
            student=student,
            paper__subject__course=student.course,
            date__range=[semester.start_date, semester.end_date]
        ).aggregate(
            avg_mark=Avg('marks_obtained'),
            total_subjects=Count('paper__subject', distinct=True)
        )

        progress_data.append({
            'semester': semester.name,
            'average': marks['avg_mark'] or 0,
            'subjects_count': marks['total_subjects'] or 0
        })

    return render(request, 'sms/reports/progressive.html', {
        'student': student,
        'progress_data': progress_data
    })


def student_progressive_report_pdf(request, pk):
    html_response = student_progressive_report(request, pk)
    html = HTML(string=html_response.content.decode('utf-8'))
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=progress_report_{pk}.pdf'
    return response


def load_semesters(request):
    academic_year_id = request.GET.get('academic_year')
    semesters = Semester.objects.filter(academic_year_id=academic_year_id).order_by('name')
    return render(request, 'sms/includes/semester_options.html', {'semesters': semesters})