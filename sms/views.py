from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import csv
import pandas as pd
from io import BytesIO

from .models import (
    Course, Student, Mark, Subject,
    Attendance, FeeStructure, Payment
)
from .forms import (
    CourseForm, StudentForm, MarkForm,
    SubjectForm, StudentUpdateForm,
    AttendanceForm, FeeStructureForm, PaymentForm
)


# ========== Subject Views ==========
class SubjectListView(ListView):
    model = Subject
    template_name = 'sms/subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 20
    ordering = ['code']


class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('subject_list')


# ========== Course Views ==========
class CourseListView(ListView):
    model = Course
    template_name = 'sms/course_list.html'
    context_object_name = 'courses'
    paginate_by = 15


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('course_list')


# ========== Student Views ==========
class StudentListView(ListView):
    model = Student
    template_name = 'sms/student_list.html'
    context_object_name = 'students'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related('course')
        course_id = self.request.GET.get('course')
        year = self.request.GET.get('year')
        semester = self.request.GET.get('semester')

        if course_id:
            queryset = queryset.filter(course__id=course_id)
        if year:
            queryset = queryset.filter(year_of_study=year)
        if semester:
            queryset = queryset.filter(semester=semester)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['years'] = Student.YEAR_CHOICES
        context['semesters'] = Student.SEMESTER_CHOICES
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'sms/student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object

        context['marks'] = Mark.objects.filter(student=student)
        context['attendance'] = Attendance.objects.filter(student=student).order_by('-date')[:30]
        context['payments'] = Payment.objects.filter(student=student).order_by('-payment_date')[:10]

        return context


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('student_list')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('student_list')


# ========== Mark Views ==========
class MarkCreateView(CreateView):
    model = Mark
    form_class = MarkForm
    template_name = 'sms/generic_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = get_object_or_404(Student, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('student_detail', kwargs={'pk': self.kwargs['pk']})


class MarkListView(ListView):
    model = Mark
    template_name = 'sms/mark_list.html'
    context_object_name = 'marks'
    paginate_by = 50


# ========== Attendance Views ==========
class AttendanceListView(ListView):
    model = Attendance
    template_name = 'sms/attendance_list.html'
    context_object_name = 'attendance_records'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student', 'subject')
        student_id = self.request.GET.get('student')
        subject_id = self.request.GET.get('subject')

        if student_id:
            queryset = queryset.filter(student__id=student_id)
        if subject_id:
            queryset = queryset.filter(subject__id=subject_id)

        return queryset


class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('attendance_list')


# ========== Financial Views ==========
class FeeStructureListView(ListView):
    model = FeeStructure
    template_name = 'sms/fee_structure_list.html'
    context_object_name = 'fee_structures'
    ordering = ['-academic_year']


class FeeStructureCreateView(CreateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('fee_structure_list')


class PaymentListView(ListView):
    model = Payment
    template_name = 'sms/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 50
    ordering = ['-payment_date']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student')
        student_id = self.request.GET.get('student')

        if student_id:
            queryset = queryset.filter(student__id=student_id)

        return queryset


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('payment_list')


# ========== Report Generation ==========
def student_academic_report(request):
    students = Student.objects.select_related('course').prefetch_related(
        Prefetch('enrolled_subjects', queryset=Subject.objects.all()),
        Prefetch('mark_set', queryset=Mark.objects.select_related('subject'))
    )
    return render(request, 'sms/academic_report.html', {
        'students': students,
        'years': Student.YEAR_CHOICES,
        'semesters': Student.SEMESTER_CHOICES
    })


def generate_student_report_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)

    # Get related data
    marks = Mark.objects.filter(student=student).select_related('subject')
    attendance = Attendance.objects.filter(student=student).order_by('-date')[:30]
    payments = Payment.objects.filter(student=student).order_by('-payment_date')[:10]

    html = render_to_string('sms/pdf_report.html', {
        'student': student,
        'marks': marks,
        'attendance': attendance,
        'payments': payments
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="student_{pk}_report.pdf"'

    HTML(string=html).write_pdf(response)
    return response


# ========== Data Export ==========
def export_data(request, format_type, model_name):
    model_map = {
        'students': (Student, ['admission_number', 'first_name', 'last_name',
                               'course__name', 'year_of_study', 'semester']),
        'courses': (Course, ['name', 'code', 'duration_years']),
        'marks': (Mark, ['student__admission_number', 'subject__name',
                         'score', 'is_absent', 'date_recorded']),
        'attendance': (Attendance, ['student__admission_number', 'date',
                                    'subject__name', 'status']),
        'payments': (Payment, ['student__admission_number', 'amount',
                               'payment_date', 'payment_method']),
        'feestructures': (FeeStructure, ['course__name', 'academic_year',
                                         'tuition_fee', 'registration_fee'])
    }

    model_data = model_map.get(model_name.lower())
    if not model_data:
        return HttpResponse("Invalid model", status=400)

    model, fields = model_data
    queryset = model.objects.all().values_list(*fields)
    columns = [f.replace('__', ' ').title() for f in fields]

    # CSV Export
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_name}_export.csv"'

        writer = csv.writer(response)
        writer.writerow(columns)
        for row in queryset:
            writer.writerow(row)
        return response

    # Excel Export
    elif format_type == 'excel':
        df = pd.DataFrame(list(queryset), columns=columns)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Export')

        response = HttpResponse(output.getvalue(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{model_name}_export.xlsx"'
        return response

    return HttpResponse("Invalid format", status=400)


# ========== Base Views ==========
class BaseCreateView(CreateView):
    template_name = 'sms/generic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'model': {
                'verbose_name': self.model._meta.verbose_name
            },
            'success_url': self.success_url
        }
        return context


class BaseUpdateView(UpdateView):
    template_name = 'sms/generic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'model': {
                'verbose_name': self.model._meta.verbose_name
            },
            'success_url': self.success_url
        }
        return context