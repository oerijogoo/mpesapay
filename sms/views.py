from django.db.models.functions import Concat, ExtractYear, ExtractMonth, TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, ExpressionWrapper, FloatField
from weasyprint import HTML
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Student, Mark, Paper
from .forms import BulkMarkForm
import csv
from django.shortcuts import render
from django.http import HttpRequest
from .models import Paper



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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Student, Mark, Paper
from .forms import BulkMarkForm
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
import csv


def bulk_mark_entry(request):
    def process_mark(student_id, mark_value, paper):
        try:
            student = Student.objects.get(pk=student_id)
            mark_value = mark_value.strip()

            if not mark_value:
                return False  # Skip empty values

            mark_decimal = Decimal(mark_value)

            if mark_decimal > paper.max_mark:
                raise ValidationError(
                    f"Mark {mark_decimal} exceeds maximum {paper.max_mark}"
                )
            if mark_decimal < 0:
                raise ValidationError("Marks cannot be negative")

            Mark.objects.update_or_create(
                student=student,
                paper=paper,
                defaults={'marks_obtained': mark_decimal}
            )
            return True

        except Student.DoesNotExist:
            raise ValidationError("Student does not exist")
        except InvalidOperation:
            raise ValidationError(f"Invalid number: {mark_value}")
        except Exception as e:
            raise ValidationError(str(e))

    if request.method == 'POST':
        form = BulkMarkForm(request.POST, request.FILES)

        # Manually update paper queryset based on submitted subject
        if 'subject' in request.POST:
            try:
                subject_id = int(request.POST.get('subject'))
                form.fields['paper'].queryset = Paper.objects.filter(subject_id=subject_id)
            except (ValueError, TypeError):
                pass

        if form.is_valid():
            try:
                with transaction.atomic():
                    paper = form.cleaned_data['paper']
                    entry_type = form.cleaned_data['entry_type']
                    count = 0
                    error_messages = []
                    header_found = False

                    if entry_type == 'bulk' and 'csv_file' in request.FILES:
                        csv_file = request.FILES['csv_file']
                        decoded_file = csv_file.read().decode('utf-8-sig').splitlines()

                        # Handle CSV header
                        if decoded_file:
                            header = decoded_file[0].lower().replace(' ', '')
                            if 'admission_number' in header and 'marks_obtained' in header:
                                header_found = True
                                decoded_file = decoded_file[1:]

                        reader = csv.DictReader(
                            decoded_file,
                            fieldnames=['admission_number', 'marks_obtained']
                        )

                        for row_num, row in enumerate(reader, start=1):
                            actual_line = row_num + (1 if header_found else 0)
                            try:
                                admission_number = row['admission_number'].strip()
                                marks = row['marks_obtained'].strip()

                                if not admission_number:
                                    raise ValidationError("Missing admission number")
                                if not marks:
                                    raise ValidationError("Missing marks value")

                                student = Student.objects.get(admission_number=admission_number)
                                if process_mark(student.id, marks, paper):
                                    count += 1
                            except Exception as e:
                                error_messages.append(f"CSV Line {actual_line}: {str(e)}")

                    else:  # Single entry mode
                        for key, value in request.POST.items():
                            if key.startswith('student_'):
                                student_id = key.split('_')[1]
                                try:
                                    if value.strip():  # Skip empty inputs
                                        if process_mark(student_id, value, paper):
                                            count += 1
                                except Exception as e:
                                    error_messages.append(f"Student {student_id}: {str(e)}")

                    # Show results
                    if count > 0:
                        messages.success(request, f"Saved {count} marks for {paper.name}")
                    if error_messages:
                        messages.error(request, f"Errors ({len(error_messages)}):")
                        for err in error_messages[:5]:
                            messages.error(request, f"- {err}")
                        if len(error_messages) > 5:
                            messages.error(request, f"- ... and {len(error_messages) - 5} more")

                    return redirect('sms:bulk_mark_entry')

            except Exception as e:
                messages.error(request, f"System Error: {str(e)}")
        else:
            # Show form errors in detail
            form_errors = []
            for field, errors in form.errors.items():
                for error in errors:
                    field_name = field.replace('_', ' ').title()
                    form_errors.append(f"{field_name}: {error}")
            messages.error(request, "Form errors: " + ", ".join(form_errors))
    else:
        form = BulkMarkForm()

    return render(request, 'sms/bulk_mark_entry.html', {
        'form': form
    })


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



# Grade CRUD Views
def grade_list(request):
    grades = Grade.objects.all().order_by('-min_mark')
    return render(request, 'sms/grade_list.html', {'grades': grades})

def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade created successfully!')
            return redirect('sms:grade_list')
    else:
        form = GradeForm()
    return render(request, 'sms/grade_form.html', {'form': form})

def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated successfully!')
            return redirect('sms:grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'sms/grade_form.html', {'form': form})

def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted successfully!')
        return redirect('sms:grade_list')
    return render(request, 'sms/grade_confirm_delete.html', {'grade': grade})


def paper_list(request):
    papers = Paper.objects.select_related('subject').order_by('subject__name')
    return render(request, 'sms/paper_list.html', {'papers': papers})

def paper_create(request):
    if request.method == 'POST':
        form = PaperForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paper created successfully!')
            return redirect('sms:paper_list')
    else:
        form = PaperForm()
    return render(request, 'sms/paper_form.html', {'form': form})

def paper_update(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    if request.method == 'POST':
        form = PaperForm(request.POST, instance=paper)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paper updated successfully!')
            return redirect('sms:paper_list')
    else:
        form = PaperForm(instance=paper)
    return render(request, 'sms/paper_form.html', {'form': form})

def paper_delete(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    if request.method == 'POST':
        paper.delete()
        messages.success(request, 'Paper deleted successfully!')
        return redirect('sms:paper_list')
    return render(request, 'sms/paper_confirm_delete.html', {'paper': paper})


def load_papers(request: HttpRequest):
    subject_id = request.GET.get('subject')
    papers = Paper.objects.none()

    if subject_id and subject_id.isdigit():
        papers = Paper.objects.filter(subject_id=int(subject_id)).order_by('name')

    return render(request, 'sms/includes/paper_options.html', {
        'papers': papers
    })

# views.py
def load_students(request):
    paper_id = request.GET.get('paper')
    students = Student.objects.none()
    paper = None
    error = None

    try:
        if paper_id:
            paper = Paper.objects.get(pk=paper_id)
            students = Student.objects.filter(
                course__subjects=paper.subject
            ).select_related('course', 'academic_year').order_by('admission_number')

            if not students.exists():
                error = "No students enrolled in courses offering this paper"

    except Paper.DoesNotExist:
        error = "Invalid paper selection"
    except Exception as e:
        error = f"Error loading students: {str(e)}"

    return render(request, 'sms/includes/student_list.html', {
        'students': students,
        'paper': paper,
        'error': error
    })


def generate_report_data(student, academic_year, semester=None):
    """Generate structured report data for a student"""
    # Determine date range based on report type
    if semester:
        start_date = semester.start_date
        end_date = semester.end_date
    else:
        start_date = academic_year.start_date
        end_date = academic_year.end_date

    report_data = {
        'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'subjects': [],
        'overall': {}
    }

    # Get all subjects for the student's course
    subjects = student.course.subjects.all()

    for subject in subjects:
        marks = Mark.objects.filter(
            student=student,
            paper__subject=subject,
            date__range=(start_date, end_date)
        ).select_related('paper')

        papers_data = []
        total_marks = 0
        max_total = 0

        for mark in marks:
            papers_data.append({
                'paper': mark.paper.name,
                'marks': mark.marks_obtained,
                'max': mark.paper.max_mark,
                'grade': mark.grade
            })
            total_marks += mark.marks_obtained
            max_total += mark.paper.max_mark

        if marks.exists():
            average = total_marks / marks.count()

            report_data['subjects'].append({
                'subject': subject,
                'papers': papers_data,
                'average': average,
                'grade': Grade.get_grade(average),
                'total_marks': total_marks,
                'max_total': max_total
            })

    # Calculate overall averages
    if report_data['subjects']:
        overall_avg = sum(s['average'] for s in report_data['subjects']) / len(report_data['subjects'])
        report_data['overall'] = {
            'average': overall_avg,
            'grade': Grade.get_grade(overall_avg),
            'total_marks': sum(s['total_marks'] for s in report_data['subjects']),
            'max_total': sum(s['max_total'] for s in report_data['subjects'])
        }

    return report_data


def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = ReportForm(request.GET or None)
    report_data = None

    if form.is_valid():
        academic_year = form.cleaned_data['academic_year']
        semester = form.cleaned_data['semester'] if form.cleaned_data['report_type'] == 'semester' else None

        report_data = generate_report_data(
            student,
            academic_year,
            semester
        )

    return render(request, 'sms/student_report.html', {
        'student': student,
        'form': form,
        'report_data': report_data
    })
def student_report_list(request):
    students = Student.objects.select_related('course').all()
    return render(request, 'sms/reports/student_list.html', {
        'students': students
    })


# sms/views.py
from django.core.paginator import Paginator


from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Course, AcademicYear

def course_report_list(request):
    # Initial queryset
    courses = Course.objects.annotate(
        student_count=Count('student'),
        subject_count=Count('subjects')
    ).order_by('name')

    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query)
        )

    # Filter by academic year
    academic_year = request.GET.get('year')
    if academic_year:
        courses = courses.filter(
            student__academic_year_id=academic_year
        ).distinct()

    # Get available academic years for filter dropdown
    academic_years = AcademicYear.objects.annotate(
        course_count=Count('student__course', distinct=True)
    ).order_by('-start_date')

    # Pagination
    paginator = Paginator(courses, 25)  # Show 25 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sms/reports/course_list.html', {
        'page_obj': page_obj,
        'search_query': search_query or '',
        'academic_years': academic_years,
        'selected_year': academic_year or ''
    })


from django.db.models import Avg, Count, F


def course_report(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Get students with their total marks using the correct related_name
    students = course.student_set.annotate(
        total_marks=Sum('marks__marks_obtained')
    ).select_related('academic_year', 'semester')

    # Get subjects with performance data using correct relationships
    subjects = course.subjects.annotate(
        average_score=Avg('papers__marks__marks_obtained'),  # Changed to 'papers__marks__'
        total_students=Count('papers__marks__student', distinct=True)
    )

    # Calculate overall statistics
    total_students = students.count()
    overall_average = subjects.aggregate(
        avg=Avg('average_score')
    )['avg'] or 0

    overall_stats = {
        'total_students': total_students,
        'average_grade': Grade.get_grade(overall_average),
        'top_subject': subjects.order_by(F('average_score').desc(nulls_last=True)).first()
    }

    return render(request, 'sms/reports/course_report.html', {
        'course': course,
        'students': students,
        'subjects': subjects,
        'overall_stats': overall_stats
    })

def semester_report_list(request):
    semesters = Semester.objects.select_related('academic_year').annotate(
        course_count=Count('student__course', distinct=True),
        student_count=Count('student', distinct=True)
    ).order_by('-academic_year__start_date', 'start_date')

    return render(request, 'sms/reports/semester_list.html', {
        'semesters': semesters
    })


from django.shortcuts import render, get_object_or_404
from .models import Semester, Course, Mark

from django.db.models import Avg, Count, Sum
from django.shortcuts import render, get_object_or_404

from django.db.models import Avg, Count, Sum, Value
from django.db.models.functions import Concat


def semester_report(request, semester_id):
    semester = get_object_or_404(Semester.objects.select_related('academic_year'), pk=semester_id)

    courses = Course.objects.filter(
        student__semester=semester
    ).annotate(
        total_students=Count('student', distinct=True),
        average_marks=Avg('student__marks__marks_obtained')  # Correct related_name
    ).distinct()

    top_students = (
        Mark.objects
        .filter(student__semester=semester)
        .values('student')
        .annotate(
            total_marks=Sum('marks_obtained'),
            full_name=Concat('student__first_name', Value(' '), 'student__last_name')
        )
        .order_by('-total_marks')[:5]
    )

    # Calculate total students
    total_students = courses.aggregate(
        total=Sum('total_students')
    ).get('total', 0) or 0

    return render(request, 'sms/reports/semester_report.html', {
        'semester': semester,
        'courses': courses,
        'top_students': top_students,
        'total_students': total_students
    })


from django.db.models import Count, Avg, Q, Value, FloatField
from django.db.models.functions import Concat, Cast
from django.http import JsonResponse
from django.shortcuts import render
import json

# views.py
from django.http import JsonResponse
from django.db.models import Count, Avg, F, Value, FloatField
from django.db.models.functions import Concat, Cast
import json
from decimal import Decimal


def convert_decimals(obj):
    """Recursively convert Decimals to floats"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    return obj


from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, F, Value, FloatField
from django.db.models.functions import Concat, Cast
from decimal import Decimal
import json
from .models import AcademicYear, Course, Semester, Subject, Mark, Student


from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    return obj


from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, F, Value, FloatField, Q
from django.db.models.functions import Concat, Cast
from decimal import Decimal
import json
from .models import AcademicYear, Course, Semester, Subject, Mark, Student

def convert_decimals(obj):
    """Recursively convert Decimals to floats"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    return obj

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, F, Value, FloatField, Q
from django.db.models.functions import Concat, Cast
from decimal import Decimal
import json
from .models import AcademicYear, Course, Semester, Subject, Mark, Student
def convert_decimals(obj):
    """Recursively convert Decimals to floats"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    return obj


from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, F, Value, FloatField
from django.db.models.functions import Concat, Cast
from decimal import Decimal
import json
from .models import AcademicYear, Course, Semester, Subject, Mark, Student


from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    return obj


from django.db.models import Q

def dashboard(request):
    try:
        # Get filter parameters
        ay_id = request.GET.get('academic_year')
        course_id = request.GET.get('course')
        semester_id = request.GET.get('semester')
        subject_id = request.GET.get('subject')

        # Grade Distribution Data
        grade_data = Mark.objects.filter(
            student__academic_year=ay_id if ay_id else Q(),
            student__course=course_id if course_id else Q(),
            student__semester=semester_id if semester_id else Q(),
            paper__subject=subject_id if subject_id else Q()
        ).values('grade__grade').annotate(
            count=Count('id')
        ).order_by('grade__min_mark')

        # Course Enrollment Data
        enrollment_data = Student.objects.filter(
            academic_year=ay_id if ay_id else Q(),
            semester=semester_id if semester_id else Q(),
            course__subjects=subject_id if subject_id else Q()
        ).values('course__name').annotate(
            total=Count('id')
        ).order_by('-total')[:10]

        # Student Performance Data
        performance_data = Student.objects.filter(
            academic_year=ay_id if ay_id else Q(),
            course=course_id if course_id else Q(),
            semester=semester_id if semester_id else Q(),
            marks__paper__subject=subject_id if subject_id else Q()
        ).annotate(
            full_name=Concat(F('first_name'), Value(' '), F('last_name')),
            avg_score=Cast(Avg('marks__marks_obtained'), FloatField())
        ).values('full_name', 'avg_score', 'course__name').distinct().order_by('-avg_score')[:10]

        context = {
            'grade_data': json.dumps(convert_decimals(list(grade_data))),
            'enrollment_data': json.dumps(convert_decimals(list(enrollment_data))),
            'performance_data': json.dumps(convert_decimals(list(performance_data))),
            'filters': {
                'academic_years': AcademicYear.objects.values(),
                'courses': Course.objects.values(),
                'semesters': Semester.objects.values(),
                'subjects': Subject.objects.values()
            }
        }
        return render(request, 'sms/dashboard.html', context)

    except Exception as e:
        return render(request, 'sms/error.html', {'error': str(e)})


def get_filtered_data(request):
    try:
        # Get filter parameters
        ay_id = request.GET.get('academic_year')
        course_id = request.GET.get('course')
        semester_id = request.GET.get('semester')
        subject_id = request.GET.get('subject')

        # Build filters dynamically
        grade_filter = Q()
        enrollment_filter = Q()
        performance_filter = Q()

        # Grade Distribution Data
        if ay_id: grade_filter &= Q(student__academic_year=ay_id)
        if course_id: grade_filter &= Q(student__course=course_id)
        if semester_id: grade_filter &= Q(student__semester=semester_id)
        if subject_id: grade_filter &= Q(paper__subject=subject_id)

        grade_data = list(Mark.objects.filter(grade_filter)
                          .values('grade__grade')
                          .annotate(count=Count('id'))
                          .order_by('grade__min_mark'))

        # Course Enrollment Data
        if ay_id: enrollment_filter &= Q(academic_year=ay_id)
        if semester_id: enrollment_filter &= Q(semester=semester_id)
        if subject_id: enrollment_filter &= Q(course__subjects=subject_id)

        enrollment_data = list(Student.objects.filter(enrollment_filter)
                               .values('course__name')
                               .annotate(total=Count('id'))
                               .order_by('-total')[:10])

        # Student Performance Data
        if ay_id: performance_filter &= Q(academic_year=ay_id)
        if course_id: performance_filter &= Q(course=course_id)
        if semester_id: performance_filter &= Q(semester=semester_id)
        if subject_id: performance_filter &= Q(marks__paper__subject=subject_id)

        performance_data = list(Student.objects.filter(performance_filter)
                                .annotate(
            full_name=Concat(F('first_name'), Value(' '), F('last_name')),
            avg_score=Cast(Avg('marks__marks_obtained'), FloatField())
        )
                                .values('full_name', 'avg_score', 'course__name')
                                .distinct()
                                .order_by('-avg_score')[:10])

        return JsonResponse({
            'grade_data': convert_decimals(grade_data),
            'enrollment_data': convert_decimals(enrollment_data),
            'performance_data': convert_decimals(performance_data)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)