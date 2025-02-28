from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, render
from .models import Course, Student, Mark, Subject
from .forms import CourseForm, StudentForm, MarkForm, SubjectForm, StudentUpdateForm
from django.db.models import Prefetch

class SubjectListView(ListView):
    model = Subject
    template_name = 'sms/subject_list.html'
    context_object_name = 'subjects'
    success_url = reverse_lazy('subject_list')

class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('subject_list')

class CourseListView(ListView):
    model = Course
    template_name = 'sms/course_list.html'
    context_object_name = 'courses'

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


class StudentListView(ListView):
    model = Student
    template_name = 'sms/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        course_id = self.request.GET.get('course')
        if course_id:
            return Student.objects.filter(course__id=course_id).select_related('course')
        return Student.objects.all().select_related('course')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class StudentDetailView(DetailView):
    model = Student
    template_name = 'sms/student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marks'] = Mark.objects.filter(student=self.object)
        return context


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'model': {
                'verbose_name': self.model._meta.verbose_name
            },
            'success_url': self.success_url
        }
        return context

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'sms/generic_form.html'
    success_url = reverse_lazy('student_list')

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


# views.py
class BaseCreateView(CreateView):
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = {
            'model': {
                'verbose_name': self.model._meta.verbose_name
            },
            'success_url': self.success_url
        }
        return context


def student_academic_report(request):
    students = Student.objects.select_related('course').prefetch_related(
        Prefetch('enrolled_subjects', queryset=Subject.objects.all()),
        Prefetch('mark_set', queryset=Mark.objects.select_related('subject'))
    )
    return render(request, 'sms/academic_report.html', {'students': students})


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_student_report_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)

    # Simple HTML template rendering
    html = render_to_string('sms/pdf_report.html', {'student': student})

    # Generate PDF with minimal configuration
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="student_{pk}_report.pdf"'

    HTML(string=html).write_pdf(response)
    return response



import csv
import pandas as pd
from django.http import HttpResponse
from io import BytesIO


def export_data(request, format_type, model_name):
    model_map = {
        'students': (Student, ['admission_number', 'first_name', 'last_name', 'course__name']),
        'courses': (Course, ['name', 'code', 'subjects__name']),
        'marks': (Mark, ['student__admission_number', 'subject__name', 'score', 'date_recorded']),
    }

    model_data = model_map.get(model_name.lower())
    if not model_data:
        return HttpResponse("Invalid model", status=400)

    model, fields = model_data
    queryset = model.objects.all().values_list(*fields)
    columns = [f.replace('__', ' ').title() for f in fields]

    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_name}_export.csv"'

        writer = csv.writer(response)
        writer.writerow(columns)
        for row in queryset:
            writer.writerow(row)
        return response

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