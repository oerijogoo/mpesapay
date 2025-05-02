from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.db.models import Q, Sum, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from .forms import *
import csv
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.forms import inlineformset_factory


def is_admin(user):
    return user.user_type == 'ADMIN'


def is_teacher(user):
    return user.user_type == 'TEACHER'


def is_student(user):
    return user.user_type == 'STUDENT'


def is_parent(user):
    return user.user_type == 'PARENT'


def is_staff(user):
    return user.user_type == 'STAFF'


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'ADMIN'


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'TEACHER'


# Dashboard Views
@login_required
def dashboard(request):
    context = {}

    if request.user.user_type == 'ADMIN':
        # Admin dashboard
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_staff = Staff.objects.count()
        total_parents = Parent.objects.count()

        recent_notices = Notice.objects.filter(is_active=True).order_by('-start_date')[:5]
        upcoming_events = Event.objects.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')[
                          :5]

        context.update({
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_staff': total_staff,
            'total_parents': total_parents,
            'recent_notices': recent_notices,
            'upcoming_events': upcoming_events,
        })

    elif request.user.user_type == 'TEACHER':
        # Teacher dashboard
        teacher = Teacher.objects.get(user=request.user)
        current_classes = ClassSubject.objects.filter(teacher=teacher).select_related('class_info', 'subject')

        context.update({
            'teacher': teacher,
            'current_classes': current_classes,
        })

    elif request.user.user_type == 'STUDENT':
        # Student dashboard
        student = Student.objects.get(user=request.user)
        current_class = student.current_class

        context.update({
            'student': student,
            'current_class': current_class,
        })

    elif request.user.user_type == 'PARENT':
        # Parent dashboard
        parent = Parent.objects.get(user=request.user)
        students = parent.students.all()

        context.update({
            'parent': parent,
            'students': students,
        })

    elif request.user.user_type == 'STAFF':
        # Staff dashboard
        staff = Staff.objects.get(user=request.user)

        context.update({
            'staff': staff,
        })

    return render(request, 'isms/dashboard.html', context)


# School Config Views
class SchoolConfigUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = SchoolConfig
    form_class = SchoolConfigForm
    template_name = 'isms/school_config_form.html'
    success_url = reverse_lazy('isms:dashboard')

    def get_object(self):
        return SchoolConfig.objects.first()

    def form_valid(self, form):
        messages.success(self.request, 'School configuration updated successfully.')
        return super().form_valid(form)


# Academic Year Views
class AcademicYearListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'isms/academic_year_list.html'
    context_object_name = 'academic_years'
    ordering = ['-start_date']


class AcademicYearCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'isms/academic_year_form.html'
    success_url = reverse_lazy('isms:academic_year_list')

    def form_valid(self, form):
        messages.success(self.request, 'Academic year created successfully.')
        return super().form_valid(form)


class AcademicYearUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'isms/academic_year_form.html'
    success_url = reverse_lazy('isms:academic_year_list')

    def form_valid(self, form):
        messages.success(self.request, 'Academic year updated successfully.')
        return super().form_valid(form)


class AcademicYearDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = AcademicYear
    template_name = 'isms/academic_year_confirm_delete.html'
    success_url = reverse_lazy('isms:academic_year_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Academic year deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Semester Views
class SemesterListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Semester
    template_name = 'isms/semester_list.html'
    context_object_name = 'semesters'

    def get_queryset(self):
        return Semester.objects.select_related('academic_year').order_by('-start_date')


class SemesterCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'isms/semester_form.html'
    success_url = reverse_lazy('isms:semester_list')

    def form_valid(self, form):
        messages.success(self.request, 'Semester created successfully.')
        return super().form_valid(form)


class SemesterUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'isms/semester_form.html'
    success_url = reverse_lazy('isms:semester_list')

    def form_valid(self, form):
        messages.success(self.request, 'Semester updated successfully.')
        return super().form_valid(form)


class SemesterDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Semester
    template_name = 'isms/semester_confirm_delete.html'
    success_url = reverse_lazy('isms:semester_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Semester deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Class Level Views
class ClassLevelListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ClassLevel
    template_name = 'isms/class_level_list.html'
    context_object_name = 'class_levels'
    ordering = ['order']


class ClassLevelCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'isms/class_level_form.html'
    success_url = reverse_lazy('isms:class_level_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class level created successfully.')
        return super().form_valid(form)


class ClassLevelUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'isms/class_level_form.html'
    success_url = reverse_lazy('isms:class_level_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class level updated successfully.')
        return super().form_valid(form)


class ClassLevelDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ClassLevel
    template_name = 'isms/class_level_confirm_delete.html'
    success_url = reverse_lazy('isms:class_level_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Class level deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Class Views
class ClassListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Class
    template_name = 'isms/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.select_related('class_level', 'class_teacher').order_by('class_level__order', 'name')


class ClassCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'isms/class_form.html'
    success_url = reverse_lazy('isms:class_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class created successfully.')
        return super().form_valid(form)


class ClassUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'isms/class_form.html'
    success_url = reverse_lazy('isms:class_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class updated successfully.')
        return super().form_valid(form)


class ClassDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Class
    template_name = 'isms/class_confirm_delete.html'
    success_url = reverse_lazy('isms:class_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Class deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Subject Views
class SubjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Subject
    template_name = 'isms/subject_list.html'
    context_object_name = 'subjects'
    ordering = ['name']


class SubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'isms/subject_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['papers_formset'] = PaperFormSet(self.request.POST, prefix='papers')
        else:
            context['papers_formset'] = PaperFormSet(
                queryset=Paper.objects.none(),
                prefix='papers'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        papers_formset = context['papers_formset']

        if papers_formset.is_valid():
            self.object = form.save()
            papers = papers_formset.save(commit=False)

            total_weight = sum(paper.weight for paper in papers if paper.weight)

            if total_weight != 100:
                messages.warning(
                    self.request,
                    f"Total paper weight is {total_weight}% (recommended: 100%)"
                )

            for paper in papers:
                paper.subject = self.object
                paper.save()

            for form in papers_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if 'save_and_add_another' in self.request.POST:
            return reverse('isms:subject_create')
        return reverse('isms:subject_detail', kwargs={'pk': self.object.pk})


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['name', 'code', 'weight']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'min': 0,
                'max': 100,
                'step': 1,
                'required': True
            })
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is None:
            raise forms.ValidationError("Weight is required")
        if weight < 0 or weight > 100:
            raise forms.ValidationError("Weight must be between 0 and 100")
        return weight


PaperFormSet = inlineformset_factory(
    Subject,
    Paper,
    form=PaperForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    fields=['name', 'code', 'weight']
)



class SubjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'isms/subject_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['papers_formset'] = PaperFormSet(
                self.request.POST,
                instance=self.object,
                prefix='papers'
            )
        else:
            context['papers_formset'] = PaperFormSet(
                instance=self.object,
                prefix='papers'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        papers_formset = context['papers_formset']

        if papers_formset.is_valid():
            self.object = form.save()
            papers = papers_formset.save(commit=False)

            total_weight = sum(paper.weight for paper in papers if paper.weight)

            if total_weight != 100:
                messages.warning(
                    self.request,
                    f"Total paper weight is {total_weight}% (recommended: 100%)"
                )

            for paper in papers:
                paper.subject = self.object
                paper.save()

            # Handle deleted forms
            for form in papers_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('isms:subject_detail', kwargs={'pk': self.object.pk})


class SubjectDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Subject
    template_name = 'isms/subject_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Subject: {self.object.name}"
        return context


class SubjectDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Subject
    template_name = 'isms/subject_confirm_delete.html'
    success_url = reverse_lazy('isms:subject_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Subject deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Paper Views
class PaperListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Paper
    template_name = 'isms/paper_list.html'
    context_object_name = 'papers'

    def get_queryset(self):
        return Paper.objects.select_related('subject').order_by('subject__name', 'name')


class PaperCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = 'isms/paper_form.html'
    success_url = reverse_lazy('isms:paper_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paper created successfully.')
        return super().form_valid(form)


class PaperUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Paper
    form_class = PaperForm
    template_name = 'isms/paper_form.html'
    success_url = reverse_lazy('isms:paper_list')

    def form_valid(self, form):
        messages.success(self.request, 'Paper updated successfully.')
        return super().form_valid(form)


class PaperDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Paper
    template_name = 'isms/paper_confirm_delete.html'
    success_url = reverse_lazy('isms:paper_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Paper deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Grading System Views
class GradingSystemListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = GradingSystem
    template_name = 'isms/grading_system_list.html'
    context_object_name = 'grading_systems'
    ordering = ['name']


class GradingSystemCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = GradingSystem
    form_class = GradingSystemForm
    template_name = 'isms/grading_system_form.html'
    success_url = reverse_lazy('isms:grading_system_list')

    def form_valid(self, form):
        messages.success(self.request, 'Grading system created successfully.')
        return super().form_valid(form)


class GradingSystemUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = GradingSystem
    form_class = GradingSystemForm
    template_name = 'isms/grading_system_form.html'
    success_url = reverse_lazy('isms:grading_system_list')

    def form_valid(self, form):
        messages.success(self.request, 'Grading system updated successfully.')
        return super().form_valid(form)


class GradingSystemDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = GradingSystem
    template_name = 'isms/grading_system_confirm_delete.html'
    success_url = reverse_lazy('isms:grading_system_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Grading system deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Grade Views
class GradeListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Grade
    template_name = 'isms/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.select_related('grading_system').order_by('grading_system__name', '-min_score')


class GradeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'isms/grade_form.html'
    success_url = reverse_lazy('isms:grade_list')

    def form_valid(self, form):
        messages.success(self.request, 'Grade created successfully.')
        return super().form_valid(form)


class GradeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'isms/grade_form.html'
    success_url = reverse_lazy('isms:grade_list')

    def form_valid(self, form):
        messages.success(self.request, 'Grade updated successfully.')
        return super().form_valid(form)


class GradeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Grade
    template_name = 'isms/grade_confirm_delete.html'
    success_url = reverse_lazy('isms:grade_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Grade deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Subject Grading Views
class SubjectGradingListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = SubjectGrading
    template_name = 'isms/subject_grading_list.html'
    context_object_name = 'subject_gradings'

    def get_queryset(self):
        return SubjectGrading.objects.select_related('subject', 'grading_system').order_by('subject__name')


class SubjectGradingCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = SubjectGrading
    form_class = SubjectGradingForm
    template_name = 'isms/subject_grading_form.html'
    success_url = reverse_lazy('isms:subject_grading_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject grading created successfully.')
        return super().form_valid(form)


class SubjectGradingUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = SubjectGrading
    form_class = SubjectGradingForm
    template_name = 'isms/subject_grading_form.html'
    success_url = reverse_lazy('isms:subject_grading_list')

    def form_valid(self, form):
        messages.success(self.request, 'Subject grading updated successfully.')
        return super().form_valid(form)


class SubjectGradingDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = SubjectGrading
    template_name = 'isms/subject_grading_confirm_delete.html'
    success_url = reverse_lazy('isms:subject_grading_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Subject grading deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Student Views
class StudentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Student
    template_name = 'isms/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = Student.objects.select_related('user', 'current_class').order_by('current_class__class_level__order',
                                                                                    'user__last_name')

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        class_filter = self.request.GET.get('class')
        if class_filter:
            queryset = queryset.filter(current_class_id=class_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Class.objects.all()
        return context


class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'isms/student_form.html'
    success_url = reverse_lazy('isms:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student created successfully.')
        return super().form_valid(form)


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'isms/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        context['attendance'] = Attendance.objects.filter(student=student).order_by('-date')[:10]
        context['results'] = ExamResult.objects.filter(student=student).select_related('exam', 'subject').order_by(
            '-exam__start_date')[:10]
        context['fee_payments'] = FeePayment.objects.filter(student=student).select_related('fee_structure').order_by(
            '-payment_date')[:10]
        return context


class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'isms/student_form.html'
    success_url = reverse_lazy('isms:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully.')
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'isms/student_confirm_delete.html'
    success_url = reverse_lazy('isms:student_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Student deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Teacher Views
class TeacherListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Teacher
    template_name = 'isms/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 20

    def get_queryset(self):
        queryset = Teacher.objects.select_related('user').order_by('user__last_name')

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(teacher_id__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        return queryset


class TeacherCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'isms/teacher_form.html'
    success_url = reverse_lazy('isms:teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher created successfully.')
        return super().form_valid(form)


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'isms/teacher_detail.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        context['classes'] = ClassSubject.objects.filter(teacher=teacher).select_related('class_info', 'subject')
        return context


class TeacherUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'isms/teacher_form.html'
    success_url = reverse_lazy('isms:teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Teacher updated successfully.')
        return super().form_valid(form)


class TeacherDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'isms/teacher_confirm_delete.html'
    success_url = reverse_lazy('isms:teacher_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Teacher deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Staff Views
class StaffListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Staff
    template_name = 'isms/staff_list.html'
    context_object_name = 'staffs'
    paginate_by = 20

    def get_queryset(self):
        queryset = Staff.objects.select_related('user').order_by('user__last_name')

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(staff_id__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        department_filter = self.request.GET.get('department')
        if department_filter:
            queryset = queryset.filter(department=department_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Staff.objects.values_list('department', flat=True).distinct()
        return context


class StaffCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'isms/staff_form.html'
    success_url = reverse_lazy('isms:staff_list')

    def form_valid(self, form):
        messages.success(self.request, 'Staff created successfully.')
        return super().form_valid(form)


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'isms/staff_detail.html'
    context_object_name = 'staff'


class StaffUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'isms/staff_form.html'
    success_url = reverse_lazy('isms:staff_list')

    def form_valid(self, form):
        messages.success(self.request, 'Staff updated successfully.')
        return super().form_valid(form)


class StaffDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Staff
    template_name = 'isms/staff_confirm_delete.html'
    success_url = reverse_lazy('isms:staff_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Staff deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Parent Views
class ParentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Parent
    template_name = 'isms/parent_list.html'
    context_object_name = 'parents'
    paginate_by = 20

    def get_queryset(self):
        queryset = Parent.objects.select_related('user').order_by('user__last_name')

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        return queryset


class ParentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Parent
    form_class = ParentForm
    template_name = 'isms/parent_form.html'
    success_url = reverse_lazy('isms:parent_list')

    def form_valid(self, form):
        messages.success(self.request, 'Parent created successfully.')
        return super().form_valid(form)


class ParentDetailView(LoginRequiredMixin, DetailView):
    model = Parent
    template_name = 'isms/parent_detail.html'
    context_object_name = 'parent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = self.object
        context['students'] = parent.students.all()
        return context


class ParentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Parent
    form_class = ParentForm
    template_name = 'isms/parent_form.html'
    success_url = reverse_lazy('isms:parent_list')

    def form_valid(self, form):
        messages.success(self.request, 'Parent updated successfully.')
        return super().form_valid(form)


class ParentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Parent
    template_name = 'isms/parent_confirm_delete.html'
    success_url = reverse_lazy('isms:parent_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Parent deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Class Subject Views
class ClassSubjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ClassSubject
    template_name = 'isms/class_subject_list.html'
    context_object_name = 'class_subjects'

    def get_queryset(self):
        return ClassSubject.objects.select_related('class_info', 'subject', 'teacher', 'academic_year').order_by(
            'class_info__name', 'subject__name')


class ClassSubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ClassSubject
    form_class = ClassSubjectForm
    template_name = 'isms/class_subject_form.html'
    success_url = reverse_lazy('isms:class_subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class subject created successfully.')
        return super().form_valid(form)


class ClassSubjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ClassSubject
    form_class = ClassSubjectForm
    template_name = 'isms/class_subject_form.html'
    success_url = reverse_lazy('isms:class_subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Class subject updated successfully.')
        return super().form_valid(form)


class ClassSubjectDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ClassSubject
    template_name = 'isms/class_subject_confirm_delete.html'
    success_url = reverse_lazy('isms:class_subject_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Class subject deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Attendance Views
class AttendanceListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Attendance
    template_name = 'isms/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 30

    def get_queryset(self):
        queryset = Attendance.objects.select_related('student', 'recorded_by').order_by('-date',
                                                                                        'student__user__last_name')

        student_filter = self.request.GET.get('student')
        if student_filter:
            queryset = queryset.filter(student_id=student_filter)

        date_filter = self.request.GET.get('date')
        if date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                pass

        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context


class AttendanceCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'isms/attendance_form.html'
    success_url = reverse_lazy('isms:attendance_list')

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Attendance record created successfully.')
        return super().form_valid(form)


class AttendanceUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'isms/attendance_form.html'
    success_url = reverse_lazy('isms:attendance_list')

    def form_valid(self, form):
        messages.success(self.request, 'Attendance record updated successfully.')
        return super().form_valid(form)


class AttendanceDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'isms/attendance_confirm_delete.html'
    success_url = reverse_lazy('isms:attendance_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Attendance record deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Bulk Attendance View
@login_required
@user_passes_test(is_admin)
def bulk_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        class_id = request.POST.get('class_info')

        if not date or not class_id:
            messages.error(request, 'Date and class are required.')
            return redirect('isms:bulk_attendance')

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Use YYYY-MM-DD.')
            return redirect('isms:bulk_attendance')

        class_info = get_object_or_404(Class, pk=class_id)
        students = Student.objects.filter(current_class=class_info)

        # Process attendance for each student
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            remark = request.POST.get(f'remark_{student.id}', '')

            if status:
                attendance, created = Attendance.objects.get_or_create(
                    student=student,
                    date=date_obj,
                    defaults={
                        'status': status,
                        'remark': remark,
                        'recorded_by': request.user
                    }
                )

                if not created:
                    attendance.status = status
                    attendance.remark = remark
                    attendance.save()

        messages.success(request, 'Bulk attendance recorded successfully.')
        return redirect('isms:attendance_list')

    classes = Class.objects.all()
    return render(request, 'isms/bulk_attendance.html', {'classes': classes})


# Exam Type Views
class ExamTypeListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ExamType
    template_name = 'isms/exam_type_list.html'
    context_object_name = 'exam_types'
    ordering = ['name']


class ExamTypeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'isms/exam_type_form.html'
    success_url = reverse_lazy('isms:exam_type_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam type created successfully.')
        return super().form_valid(form)


class ExamTypeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'isms/exam_type_form.html'
    success_url = reverse_lazy('isms:exam_type_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam type updated successfully.')
        return super().form_valid(form)


class ExamTypeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ExamType
    template_name = 'isms/exam_type_confirm_delete.html'
    success_url = reverse_lazy('isms:exam_type_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Exam type deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Exam Views
class ExamListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Exam
    template_name = 'isms/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        return Exam.objects.select_related('exam_type', 'academic_year', 'semester').order_by('-start_date')


class ExamCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'isms/exam_form.html'
    success_url = reverse_lazy('isms:exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam created successfully.')
        return super().form_valid(form)


class ExamDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Exam
    template_name = 'isms/exam_detail.html'
    context_object_name = 'exam'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.object
        context['results'] = ExamResult.objects.filter(exam=exam).select_related('student', 'subject')
        return context


class ExamUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'isms/exam_form.html'
    success_url = reverse_lazy('isms:exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam updated successfully.')
        return super().form_valid(form)


class ExamDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Exam
    template_name = 'isms/exam_confirm_delete.html'
    success_url = reverse_lazy('isms:exam_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Exam deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Exam Result Views
class ExamResultListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ExamResult
    template_name = 'isms/exam_result_list.html'
    context_object_name = 'exam_results'
    paginate_by = 30

    def get_queryset(self):
        queryset = ExamResult.objects.select_related(
            'exam', 'student', 'subject', 'paper', 'grade', 'recorded_by'
        ).order_by('-exam__start_date', 'student__user__last_name')

        exam_filter = self.request.GET.get('exam')
        if exam_filter:
            queryset = queryset.filter(exam_id=exam_filter)

        student_filter = self.request.GET.get('student')
        if student_filter:
            queryset = queryset.filter(student_id=student_filter)

        subject_filter = self.request.GET.get('subject')
        if subject_filter:
            queryset = queryset.filter(subject_id=subject_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = Exam.objects.all()
        context['students'] = Student.objects.all()
        context['subjects'] = Subject.objects.all()
        return context


class ExamResultCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ExamResult
    form_class = ExamResultForm
    template_name = 'isms/exam_result_form.html'
    success_url = reverse_lazy('isms:exam_result_list')

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, 'Exam result created successfully.')
        return super().form_valid(form)


class ExamResultUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ExamResult
    form_class = ExamResultForm
    template_name = 'isms/exam_result_form.html'
    success_url = reverse_lazy('isms:exam_result_list')

    def form_valid(self, form):
        messages.success(self.request, 'Exam result updated successfully.')
        return super().form_valid(form)


class ExamResultDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ExamResult
    template_name = 'isms/exam_result_confirm_delete.html'
    success_url = reverse_lazy('isms:exam_result_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Exam result deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Bulk Exam Result View
@login_required
@user_passes_test(is_admin)
def bulk_exam_result(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam')
        class_id = request.POST.get('class_info')
        subject_id = request.POST.get('subject')

        if not exam_id or not class_id or not subject_id:
            messages.error(request, 'Exam, class and subject are required.')
            return redirect('isms:bulk_exam_result')

        exam = get_object_or_404(Exam, pk=exam_id)
        class_info = get_object_or_404(Class, pk=class_id)
        subject = get_object_or_404(Subject, pk=subject_id)

        students = Student.objects.filter(current_class=class_info)

        # Process results for each student
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            paper_id = request.POST.get(f'paper_{student.id}')

            if marks:
                exam_result, created = ExamResult.objects.get_or_create(
                    exam=exam,
                    student=student,
                    subject=subject,
                    paper_id=paper_id if paper_id else None,
                    defaults={
                        'marks': marks,
                        'recorded_by': request.user
                    }
                )

                if not created:
                    exam_result.marks = marks
                    exam_result.paper_id = paper_id if paper_id else None
                    exam_result.save()

        messages.success(request, 'Bulk exam results recorded successfully.')
        return redirect('isms:exam_result_list')

    exams = Exam.objects.all()
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'isms/bulk_exam_result.html', {
        'exams': exams,
        'classes': classes,
        'subjects': subjects
    })


# Fee Type Views
class FeeTypeListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeType
    template_name = 'isms/fee_type_list.html'
    context_object_name = 'fee_types'
    ordering = ['name']


class FeeTypeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeType
    form_class = FeeTypeForm
    template_name = 'isms/fee_type_form.html'
    success_url = reverse_lazy('isms:fee_type_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fee type created successfully.')
        return super().form_valid(form)


class FeeTypeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeeType
    form_class = FeeTypeForm
    template_name = 'isms/fee_type_form.html'
    success_url = reverse_lazy('isms:fee_type_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fee type updated successfully.')
        return super().form_valid(form)


class FeeTypeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeeType
    template_name = 'isms/fee_type_confirm_delete.html'
    success_url = reverse_lazy('isms:fee_type_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fee type deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Fee Structure Views
class FeeStructureListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'isms/fee_structure_list.html'
    context_object_name = 'fee_structures'

    def get_queryset(self):
        return FeeStructure.objects.select_related('fee_type', 'class_level', 'academic_year').order_by(
            'academic_year__name', 'class_level__order')


class FeeStructureCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'isms/fee_structure_form.html'
    success_url = reverse_lazy('isms:fee_structure_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fee structure created successfully.')
        return super().form_valid(form)


class FeeStructureUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'isms/fee_structure_form.html'
    success_url = reverse_lazy('isms:fee_structure_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fee structure updated successfully.')
        return super().form_valid(form)


class FeeStructureDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeeStructure
    template_name = 'isms/fee_structure_confirm_delete.html'
    success_url = reverse_lazy('isms:fee_structure_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fee structure deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Fee Payment Views
class FeePaymentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = FeePayment
    template_name = 'isms/fee_payment_list.html'
    context_object_name = 'fee_payments'
    paginate_by = 30

    def get_queryset(self):
        queryset = FeePayment.objects.select_related(
            'student', 'fee_structure', 'received_by'
        ).order_by('-payment_date')

        student_filter = self.request.GET.get('student')
        if student_filter:
            queryset = queryset.filter(student_id=student_filter)

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(payment_date__gte=date_from_obj)
            except ValueError:
                pass

        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(payment_date__lte=date_to_obj)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context


class FeePaymentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = FeePayment
    form_class = FeePaymentForm
    template_name = 'isms/fee_payment_form.html'
    success_url = reverse_lazy('isms:fee_payment_list')

    def form_valid(self, form):
        form.instance.received_by = self.request.user
        messages.success(self.request, 'Fee payment recorded successfully.')
        return super().form_valid(form)


class FeePaymentDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = FeePayment
    template_name = 'isms/fee_payment_detail.html'
    context_object_name = 'fee_payment'


class FeePaymentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = FeePayment
    form_class = FeePaymentForm
    template_name = 'isms/fee_payment_form.html'
    success_url = reverse_lazy('isms:fee_payment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fee payment updated successfully.')
        return super().form_valid(form)


class FeePaymentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = FeePayment
    template_name = 'isms/fee_payment_confirm_delete.html'
    success_url = reverse_lazy('isms:fee_payment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fee payment deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Fee Payment Receipt
@login_required
def fee_payment_receipt(request, pk):
    fee_payment = get_object_or_404(FeePayment, pk=pk)
    school_config = SchoolConfig.objects.first()

    # Generate PDF
    html_string = render_to_string('isms/fee_payment_receipt_pdf.html', {
        'fee_payment': fee_payment,
        'school_config': school_config
    })

    html = HTML(string=html_string)
    result = html.write_pdf()

    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fee_receipt_{fee_payment.receipt_number}.pdf"'
    response.write(result)

    return response


# Promotion Views
class PromotionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Promotion
    template_name = 'isms/promotion_list.html'
    context_object_name = 'promotions'

    def get_queryset(self):
        return Promotion.objects.select_related(
            'student', 'from_class', 'to_class', 'academic_year', 'promoted_by'
        ).order_by('-academic_year__name', 'student__user__last_name')


class PromotionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'isms/promotion_form.html'
    success_url = reverse_lazy('isms:promotion_list')

    def form_valid(self, form):
        form.instance.promoted_by = self.request.user
        messages.success(self.request, 'Promotion recorded successfully.')
        return super().form_valid(form)


class PromotionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'isms/promotion_form.html'
    success_url = reverse_lazy('isms:promotion_list')

    def form_valid(self, form):
        messages.success(self.request, 'Promotion updated successfully.')
        return super().form_valid(form)


class PromotionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Promotion
    template_name = 'isms/promotion_confirm_delete.html'
    success_url = reverse_lazy('isms:promotion_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Promotion deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Bulk Promotion View
@login_required
@user_passes_test(is_admin)
def bulk_promotion(request):
    if request.method == 'POST':
        academic_year_id = request.POST.get('academic_year')
        from_class_id = request.POST.get('from_class')
        to_class_id = request.POST.get('to_class')

        if not academic_year_id or not from_class_id or not to_class_id:
            messages.error(request, 'Academic year, from class and to class are required.')
            return redirect('isms:bulk_promotion')

        academic_year = get_object_or_404(AcademicYear, pk=academic_year_id)
        from_class = get_object_or_404(Class, pk=from_class_id)
        to_class = get_object_or_404(Class, pk=to_class_id)

        students = Student.objects.filter(current_class=from_class)

        # Process promotion for each student
        for student in students:
            promotion, created = Promotion.objects.get_or_create(
                student=student,
                academic_year=academic_year,
                defaults={
                    'from_class': from_class,
                    'to_class': to_class,
                    'date': timezone.now().date(),
                    'promoted_by': request.user
                }
            )

            if not created:
                promotion.to_class = to_class
                promotion.save()

            # Update student's current class
            student.current_class = to_class
            student.save()

        messages.success(request, 'Bulk promotion processed successfully.')
        return redirect('isms:promotion_list')

    academic_years = AcademicYear.objects.all()
    classes = Class.objects.all()
    return render(request, 'isms/bulk_promotion.html', {
        'academic_years': academic_years,
        'classes': classes
    })


# Timetable Views
class TimetableListView(LoginRequiredMixin, ListView):
    model = Timetable
    template_name = 'isms/timetable_list.html'
    context_object_name = 'timetables'

    def get_queryset(self):
        queryset = Timetable.objects.select_related(
            'class_info', 'subject', 'teacher', 'academic_year'
        ).filter(is_active=True).order_by('day', 'start_time')

        if self.request.user.user_type == 'TEACHER':
            teacher = Teacher.objects.get(user=self.request.user)
            queryset = queryset.filter(teacher=teacher)
        elif self.request.user.user_type == 'STUDENT':
            student = Student.objects.get(user=self.request.user)
            if student.current_class:
                queryset = queryset.filter(class_info=student.current_class)

        class_filter = self.request.GET.get('class')
        if class_filter:
            queryset = queryset.filter(class_info_id=class_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type == 'ADMIN':
            context['classes'] = Class.objects.all()
        return context


class TimetableCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'isms/timetable_form.html'
    success_url = reverse_lazy('isms:timetable_list')

    def form_valid(self, form):
        messages.success(self.request, 'Timetable entry created successfully.')
        return super().form_valid(form)


class TimetableUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Timetable
    form_class = TimetableForm
    template_name = 'isms/timetable_form.html'
    success_url = reverse_lazy('isms:timetable_list')

    def form_valid(self, form):
        messages.success(self.request, 'Timetable entry updated successfully.')
        return super().form_valid(form)


class TimetableDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Timetable
    template_name = 'isms/timetable_confirm_delete.html'
    success_url = reverse_lazy('isms:timetable_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Timetable entry deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Notice Views
class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'isms/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True).order_by('-start_date')

        if self.request.user.user_type != 'ADMIN':
            queryset = queryset.filter(
                Q(audience='ALL') |
                Q(audience=self.request.user.user_type)
            )

        return queryset


class NoticeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'isms/notice_form.html'
    success_url = reverse_lazy('isms:notice_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Notice created successfully.')
        return super().form_valid(form)


class NoticeDetailView(LoginRequiredMixin, DetailView):
    model = Notice
    template_name = 'isms/notice_detail.html'
    context_object_name = 'notice'


class NoticeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'isms/notice_form.html'
    success_url = reverse_lazy('isms:notice_list')

    def form_valid(self, form):
        messages.success(self.request, 'Notice updated successfully.')
        return super().form_valid(form)


class NoticeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Notice
    template_name = 'isms/notice_confirm_delete.html'
    success_url = reverse_lazy('isms:notice_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Notice deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Event Views
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'isms/event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')

        if self.request.user.user_type != 'ADMIN':
            queryset = queryset.filter(
                Q(audience='ALL') |
                Q(audience=self.request.user.user_type)
            )

        return queryset


class EventCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'isms/event_form.html'
    success_url = reverse_lazy('isms:event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Event created successfully.')
        return super().form_valid(form)


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'isms/event_detail.html'
    context_object_name = 'event'


class EventUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'isms/event_form.html'
    success_url = reverse_lazy('isms:event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully.')
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Event
    template_name = 'isms/event_confirm_delete.html'
    success_url = reverse_lazy('isms:event_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Library Book Views
class LibraryBookListView(LoginRequiredMixin, ListView):
    model = LibraryBook
    template_name = 'isms/library_book_list.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        queryset = LibraryBook.objects.order_by('title')

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query) |
                Q(category__icontains=search_query)
            )

        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category=category_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LibraryBook.objects.values_list('category', flat=True).distinct()
        return context


class LibraryBookCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = LibraryBook
    form_class = LibraryBookForm
    template_name = 'isms/library_book_form.html'
    success_url = reverse_lazy('isms:library_book_list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, 'Book added successfully.')
        return super().form_valid(form)


class LibraryBookDetailView(LoginRequiredMixin, DetailView):
    model = LibraryBook
    template_name = 'isms/library_book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = BookIssue.objects.filter(book=self.object).select_related('issued_to')
        return context


class LibraryBookUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = LibraryBook
    form_class = LibraryBookForm
    template_name = 'isms/library_book_form.html'
    success_url = reverse_lazy('isms:library_book_list')

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully.')
        return super().form_valid(form)


class LibraryBookDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = LibraryBook
    template_name = 'isms/library_book_confirm_delete.html'
    success_url = reverse_lazy('isms:library_book_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Book Issue Views
class BookIssueListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = BookIssue
    template_name = 'isms/book_issue_list.html'
    context_object_name = 'book_issues'
    paginate_by = 20

    def get_queryset(self):
        queryset = BookIssue.objects.select_related('book', 'issued_to', 'issued_by').order_by('-issue_date')

        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        overdue_filter = self.request.GET.get('overdue')
        if overdue_filter == 'true':
            queryset = queryset.filter(due_date__lt=timezone.now().date(), status='ISSUED')

        return queryset


class BookIssueCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = BookIssue
    form_class = BookIssueForm
    template_name = 'isms/book_issue_form.html'
    success_url = reverse_lazy('isms:book_issue_list')

    def form_valid(self, form):
        form.instance.issued_by = self.request.user
        form.instance.status = 'ISSUED'

        # Update book availability
        book = form.cleaned_data['book']
        if book.available <= 0:
            messages.error(self.request, 'This book is not available for issue.')
            return self.form_invalid(form)

        book.available -= 1
        book.save()

        messages.success(self.request, 'Book issued successfully.')
        return super().form_valid(form)


class BookIssueUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = BookIssue
    form_class = BookIssueForm
    template_name = 'isms/book_issue_form.html'
    success_url = reverse_lazy('isms:book_issue_list')

    def form_valid(self, form):
        old_status = self.get_object().status
        new_status = form.cleaned_data['status']

        if old_status != new_status and new_status == 'RETURNED':
            # Update book availability when returned
            book = form.cleaned_data['book']
            book.available += 1
            book.save()

        messages.success(self.request, 'Book issue updated successfully.')
        return super().form_valid(form)


class BookIssueDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = BookIssue
    template_name = 'isms/book_issue_confirm_delete.html'
    success_url = reverse_lazy('isms:book_issue_list')

    def delete(self, request, *args, **kwargs):
        book_issue = self.get_object()

        # Update book availability if the book was issued
        if book_issue.status == 'ISSUED':
            book = book_issue.book
            book.available += 1
            book.save()

        messages.success(request, 'Book issue record deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Reports
@login_required
@user_passes_test(is_admin)
def reports(request):
    return render(request, 'isms/reports.html')


# Attendance Report
@login_required
@user_passes_test(is_admin)
def attendance_report(request):
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            class_info = form.cleaned_data['class_info']

            # Get attendance data
            attendance_data = Attendance.objects.filter(
                date__gte=date_from,
                date__lte=date_to,
                student__current_class=class_info
            ).values(
                'student__user__first_name',
                'student__user__last_name',
                'student__student_id',
                'status'
            ).annotate(
                total=Count('id'),
                present=Count('id', filter=Q(status='P')),
                absent=Count('id', filter=Q(status='A')),
                late=Count('id', filter=Q(status='L')),
                half_day=Count('id', filter=Q(status='H'))
            ).order_by('student__user__last_name')

            # Generate CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="attendance_report_{date_from}_{date_to}.csv"'

            writer = csv.writer(response)
            writer.writerow([
                'Student ID', 'Student Name', 'Total Days', 'Present', 'Absent', 'Late', 'Half Day'
            ])

            for row in attendance_data:
                writer.writerow([
                    row['student__student_id'],
                    f"{row['student__user__first_name']} {row['student__user__last_name']}",
                    row['total'],
                    row['present'],
                    row['absent'],
                    row['late'],
                    row['half_day']
                ])

            return response
    else:
        form = AttendanceReportForm()

    return render(request, 'isms/attendance_report.html', {'form': form})


# Exam Results Report
@login_required
@user_passes_test(is_admin)
def exam_results_report(request):
    if request.method == 'POST':
        form = ExamResultsReportForm(request.POST)
        if form.is_valid():
            exam = form.cleaned_data['exam']
            class_info = form.cleaned_data['class_info']

            # Get exam results data
            results = ExamResult.objects.filter(
                exam=exam,
                student__current_class=class_info
            ).select_related('student', 'subject').order_by('student__user__last_name', 'subject__name')

            # Generate PDF
            html_string = render_to_string('isms/exam_results_report_pdf.html', {
                'exam': exam,
                'class_info': class_info,
                'results': results
            })

            html = HTML(string=html_string)
            result = html.write_pdf()

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="exam_results_{exam.name}_{class_info.name}.pdf"'
            response.write(result)

            return response
    else:
        form = ExamResultsReportForm()

    return render(request, 'isms/exam_results_report.html', {'form': form})


# Fee Collection Report
@login_required
@user_passes_test(is_admin)
def fee_collection_report(request):
    if request.method == 'POST':
        form = FeeCollectionReportForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            fee_type = form.cleaned_data['fee_type']

            # Get fee payment data
            payments = FeePayment.objects.filter(
                payment_date__gte=date_from,
                payment_date__lte=date_to
            )

            if fee_type:
                payments = payments.filter(fee_structure__fee_type=fee_type)

            payments = payments.select_related('student', 'fee_structure').order_by('payment_date')

            total_amount = payments.aggregate(total=Sum('amount_paid'))['total'] or 0

            # Generate CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="fee_collection_{date_from}_{date_to}.csv"'

            writer = csv.writer(response)
            writer.writerow([
                'Date', 'Receipt No', 'Student ID', 'Student Name', 'Fee Type', 'Amount', 'Payment Method'
            ])

            for payment in payments:
                writer.writerow([
                    payment.payment_date.strftime('%Y-%m-%d'),
                    payment.receipt_number,
                    payment.student.student_id,
                    f"{payment.student.user.first_name} {payment.student.user.last_name}",
                    payment.fee_structure.fee_type.name,
                    payment.amount_paid,
                    payment.get_payment_method_display()
                ])

            writer.writerow([])
            writer.writerow(['Total Amount Collected:', '', '', '', '', total_amount])

            return response
    else:
        form = FeeCollectionReportForm()

    return render(request, 'isms/fee_collection_report.html', {'form': form})


# Student Progress Report
@login_required
def student_progress_report(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    # Check if the requesting user has permission to view this student's progress
    if request.user.user_type == 'PARENT':
        parent = Parent.objects.get(user=request.user)
        if student not in parent.students.all():
            return HttpResponseForbidden("You don't have permission to view this student's progress.")
    elif request.user.user_type == 'STUDENT':
        if request.user != student.user:
            return HttpResponseForbidden("You don't have permission to view this student's progress.")

    # Get all exam results for the student
    exam_results = ExamResult.objects.filter(
        student=student
    ).select_related('exam', 'subject').order_by('exam__start_date', 'subject__name')

    # Group results by exam
    grouped_results = {}
    for result in exam_results:
        if result.exam not in grouped_results:
            grouped_results[result.exam] = []
        grouped_results[result.exam].append(result)

    # Generate PDF
    html_string = render_to_string('isms/student_progress_report_pdf.html', {
        'student': student,
        'grouped_results': grouped_results
    })

    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="student_progress_{student.student_id}.pdf"'
    response.write(result)

    return response


# Custom Forms for Reports
class AttendanceReportForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class_info = forms.ModelChoiceField(queryset=Class.objects.all())


class ExamResultsReportForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exam.objects.all())
    class_info = forms.ModelChoiceField(queryset=Class.objects.all())


class FeeCollectionReportForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fee_type = forms.ModelChoiceField(queryset=FeeType.objects.all(), required=False)