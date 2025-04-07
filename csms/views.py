# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import (
    SchoolSettings, AcademicYear, Semester, AcademicLevel, Course,
    Subject, Paper, CourseSubject, GradingScale, Grade, SubjectGrading,
    Teacher, Student, Enrollment, Class, ClassSubject, ExamType, Exam,
    ExamSchedule, Mark, GradeAllocation, AcademicReport, FeeType,
    FeeStructure, StudentFee, AcademicCalendar, Attendance, Notification
)
from .forms import (
    SchoolSettingsForm, AcademicYearForm, SemesterForm, AcademicLevelForm,
    CourseForm, SubjectForm, PaperForm, PaperFormSet, CourseSubjectForm,
    GradingScaleForm, GradeForm, SubjectGradingForm, TeacherForm, TeacherUserForm,
    StudentForm, StudentUserForm, EnrollmentForm, ClassForm, ClassSubjectForm,
    ExamTypeForm, ExamForm, ExamScheduleForm, MarkForm, GradeAllocationForm,
    AcademicReportForm, FeeTypeForm, FeeStructureForm, StudentFeeForm,
    AcademicCalendarForm, AttendanceForm, NotificationForm, BulkMarkEntryForm,
    BulkStudentCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


# ======================
# Base View Classes
# ======================
class BaseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'crud/create.html'
    success_message = "%(name)s was created successfully"
    list_url_name = None  # This should be set in child views
    detail_url_name = None  # Optional for detail views

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        if self.list_url_name:
            context['list_url'] = self.list_url_name  # Just pass the name, not reverse_lazy
        return context

    def get_success_url(self):
        if self.detail_url_name and hasattr(self, 'object'):
            return reverse_lazy(self.detail_url_name, kwargs={'pk': self.object.pk})
        elif self.list_url_name:
            return reverse_lazy(self.list_url_name)
        raise ImproperlyConfigured(
            "No URL to redirect to. Either provide a detail_url_name or list_url_name."
        )

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=str(self.object),
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        messages.success(self.request, success_message)
        return response


class BaseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'crud/update.html'
    success_message = "%(name)s was updated successfully"
    list_url_name = None  # Must be set in child views
    detail_url_name = None  # Optional for detail views

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name
        if self.list_url_name:
            context['list_url'] = self.list_url_name  # Pass the URL name directly
        return context

    def get_success_url(self):
        if self.detail_url_name and hasattr(self, 'object'):
            return reverse_lazy(self.detail_url_name, kwargs={'pk': self.object.pk})
        elif self.list_url_name:
            return reverse_lazy(self.list_url_name)
        raise ImproperlyConfigured(
            "No URL to redirect to. Either provide a detail_url_name or list_url_name."
        )

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=str(self.object),
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        messages.success(self.request, success_message)
        return response


class BaseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'crud/delete.html'
    success_message = "%(name)s was deleted successfully"
    list_url_name = None

    def get_success_url(self):
        if self.list_url_name:
            return reverse_lazy(self.list_url_name)
        raise ImproperlyConfigured("No URL to redirect to. Provide a list_url_name.")

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=str(self.object),
        )

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.get_success_message({'name': str(obj)}))
        return super().delete(request, *args, **kwargs)


# ======================
# School Configuration Views
# ======================
class SchoolSettingsView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SchoolSettings
    form_class = SchoolSettingsForm
    template_name = 'configuration/school_settings.html'
    permission_required = 'csms.change_schoolsettings'
    success_url = reverse_lazy('csms:school_settings')  # Add the namespace here

    def get_object(self):
        return SchoolSettings.objects.first()

    def form_valid(self, form):
        messages.success(self.request, "School settings updated successfully")
        return super().form_valid(form)


# ======================
# Academic Structure Views
# ======================
class AcademicYearListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'academic/academic_year_list.html'
    permission_required = 'csms.view_academicyear'
    context_object_name = 'academic_years'


class AcademicYearCreateView(BaseCreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    permission_required = 'csms.add_academicyear'
    list_url_name = 'csms:academic_year_list'  # Make sure this matches your URL pattern name


class AcademicYearUpdateView(BaseUpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    permission_required = 'csms.change_academicyear'
    list_url_name = 'csms:academic_year_list'


class AcademicYearDeleteView(BaseDeleteView):
    model = AcademicYear
    permission_required = 'csms.delete_academicyear'
    list_url_name = 'sms:academic_year_list'


class SemesterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Semester
    template_name = 'academic/semester_list.html'
    permission_required = 'csms.view_semester'
    context_object_name = 'sms:semesters'

    def get_queryset(self):
        return super().get_queryset().select_related('academic_year')


class SemesterCreateView(BaseCreateView):
    model = Semester
    form_class = SemesterForm
    permission_required = 'csms.add_semester'
    list_url_name = 'csms:semester_list'


class SemesterUpdateView(BaseUpdateView):
    model = Semester
    form_class = SemesterForm
    permission_required = 'csms.change_semester'
    list_url_name = 'csms:semester_list'


class SemesterDeleteView(BaseDeleteView):
    model = Semester
    permission_required = 'csms.delete_semester'
    list_url_name = 'csms:semester_list'


class AcademicLevelListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AcademicLevel
    template_name = 'academic/academic_level_list.html'
    permission_required = 'csms.view_academiclevel'
    context_object_name = 'academic_levels'  # Remove 'csms:' prefix
    paginate_by = 10  # Add pagination if needed


class AcademicLevelCreateView(BaseCreateView):
    model = AcademicLevel
    form_class = AcademicLevelForm
    permission_required = 'csms.add_academiclevel'
    list_url_name = 'csms:academic_level_list'


class AcademicLevelUpdateView(BaseUpdateView):
    model = AcademicLevel
    form_class = AcademicLevelForm
    permission_required = 'csms.change_academiclevel'
    list_url_name = 'csms:academic_level_list'


class AcademicLevelDeleteView(BaseDeleteView):
    model = AcademicLevel
    permission_required = 'csms.delete_academiclevel'
    list_url_name = 'csms:academic_level_list'


# ======================
# Course and Subject Views
# ======================
class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    template_name = 'academic/course_list.html'
    permission_required = 'csms.view_course'
    context_object_name = 'courses'

    def get_queryset(self):
        return super().get_queryset().select_related('academic_level')


class CourseCreateView(BaseCreateView):
    model = Course
    form_class = CourseForm
    permission_required = 'csms.add_course'
    list_url_name = 'csms:course_list'
    detail_url_name = 'csms:course_detail'  # Add namespace



class CourseUpdateView(BaseUpdateView):
    model = Course
    form_class = CourseForm
    permission_required = 'csms.change_course'
    list_url_name = 'csms:course_list'  # Add namespace
    detail_url_name = 'csms:course_detail'  # Add namespace


class CourseDeleteView(BaseDeleteView):
    model = Course
    permission_required = 'csms.delete_course'
    list_url_name = 'course_list'


class CourseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    template_name = 'academic/course_detail.html'
    permission_required = 'csms.view_course'
    context_object_name = 'course'


class SubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Subject
    template_name = 'academic/subject_list.html'
    permission_required = 'csms.view_subject'
    context_object_name = 'subjects'


class SubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academic/subject_create.html'
    permission_required = 'csms.add_subject'
    success_url = reverse_lazy('csms:subject_list')  # Add namespace
    list_url_name = 'csms:subject_list'  # Add namespace
    detail_url_name = 'csms:subject_detail'  # Add namespace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['paper_formset'] = PaperFormSet(self.request.POST)
        else:
            context['paper_formset'] = PaperFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        paper_formset = context['paper_formset']

        with transaction.atomic():
            self.object = form.save()

            if paper_formset.is_valid():
                paper_formset.instance = self.object
                paper_formset.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class SubjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academic/subject_update.html'
    permission_required = 'csms.change_subject'
    success_url = reverse_lazy('csms:subject_list')  # Add namespace
    list_url_name = 'csms:subject_list'  # Add namespace
    detail_url_name = 'csms:subject_detail'  # Add namespace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['paper_formset'] = PaperFormSet(self.request.POST, instance=self.object)
        else:
            context['paper_formset'] = PaperFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        paper_formset = context['paper_formset']

        with transaction.atomic():
            self.object = form.save()

            if paper_formset.is_valid():
                paper_formset.instance = self.object
                paper_formset.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class SubjectDeleteView(BaseDeleteView):
    model = Subject
    permission_required = 'csms.delete_subject'
    list_url_name = 'csms:subject_list'  # Add namespace


class SubjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Subject
    template_name = 'academic/subject_detail.html'
    permission_required = 'csms.view_subject'
    context_object_name = 'subject'


class CourseSubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CourseSubject
    template_name = 'academic/course_subject_list.html'
    permission_required = 'csms.view_coursesubject'
    context_object_name = 'course_subjects'

    def get_queryset(self):
        return super().get_queryset().select_related('course', 'subject', 'semester')


class CourseSubjectCreateView(BaseCreateView):
    model = CourseSubject
    form_class = CourseSubjectForm
    permission_required = 'csms.add_coursesubject'
    list_url_name = 'csms:course_subject_list'  # Add namespace


class CourseSubjectUpdateView(BaseUpdateView):
    model = CourseSubject
    form_class = CourseSubjectForm
    permission_required = 'csms.change_coursesubject'
    list_url_name = 'csms:course_subject_list'  # Add namespace


class CourseSubjectDeleteView(BaseDeleteView):
    model = CourseSubject
    permission_required = 'csms.delete_coursesubject'
    list_url_name = 'csms:course_subject_list'  # Add namespace


# ======================
# Grading System Views
# ======================
class GradingScaleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = GradingScale
    template_name = 'grading/grading_scale_list.html'
    permission_required = 'csms.view_gradingscale'
    context_object_name = 'csms:grading_scales'


class GradingScaleCreateView(BaseCreateView):
    model = GradingScale
    form_class = GradingScaleForm
    permission_required = 'csms.add_gradingscale'
    list_url_name = 'csms:grading_scale_list'
    detail_url_name = 'csms:grading_scale_detail'


class GradingScaleUpdateView(BaseUpdateView):
    model = GradingScale
    form_class = GradingScaleForm
    permission_required = 'csms.change_gradingscale'
    list_url_name = 'csms:grading_scale_list'
    detail_url_name = 'csms:grading_scale_detail'


class GradingScaleDeleteView(BaseDeleteView):
    model = GradingScale
    permission_required = 'csms.delete_gradingscale'
    list_url_name = 'csms:grading_scale_list'


class GradingScaleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = GradingScale
    template_name = 'grading/grading_scale_detail.html'
    permission_required = 'csms.view_gradingscale'
    context_object_name = 'csms:grading_scale'


class GradeCreateView(BaseCreateView):
    model = Grade
    form_class = GradeForm
    permission_required = 'csms.add_grade'
    template_name = 'grading/grade_form.html'

    def get_initial(self):
        initial = super().get_initial()
        grading_scale_id = self.kwargs.get('grading_scale_id')
        if grading_scale_id:
            initial['grading_scale'] = get_object_or_404(GradingScale, pk=grading_scale_id)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grading_scale_id = self.kwargs.get('grading_scale_id')
        if grading_scale_id:
            context['grading_scale'] = get_object_or_404(GradingScale, pk=grading_scale_id)
        return context

    def get_success_url(self):
        return reverse_lazy('csms:grading_scale_detail', kwargs={'pk': self.object.grading_scale.pk})


class GradeUpdateView(BaseUpdateView):
    model = Grade
    form_class = GradeForm
    permission_required = 'csms.change_grade'
    template_name = 'grading/grade_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grading_scale'] = self.object.grading_scale  # Add grading_scale to context
        return context

    def get_success_url(self):
        return reverse_lazy('csms:grading_scale_detail', kwargs={'pk': self.object.grading_scale.pk})


class GradeDeleteView(BaseDeleteView):
    model = Grade
    permission_required = 'csms.delete_grade'
    template_name = 'grading/grade_confirm_delete.html'
    detail_url_name = 'csms:grading_scale_detail'

    def get_success_url(self):
        return reverse_lazy('csms:grading_scale_detail', kwargs={'pk': self.object.grading_scale.pk})


class SubjectGradingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SubjectGrading
    template_name = 'grading/subject_grading_list.html'
    permission_required = 'csms.view_subjectgrading'
    context_object_name = 'csms:subject_gradings'

    def get_queryset(self):
        return super().get_queryset().select_related('subject', 'grading_scale')


class SubjectGradingCreateView(BaseCreateView):
    model = SubjectGrading
    form_class = SubjectGradingForm
    permission_required = 'csms.add_subjectgrading'
    list_url_name = 'csms:subject_grading_list'


class SubjectGradingUpdateView(BaseUpdateView):
    model = SubjectGrading
    form_class = SubjectGradingForm
    permission_required = 'csms.change_subjectgrading'
    list_url_name = 'csms:subject_grading_list'


class SubjectGradingDeleteView(BaseDeleteView):
    model = SubjectGrading
    permission_required = 'csms.delete_subjectgrading'
    list_url_name = 'csms:subject_grading_list'


# ======================
# People Management Views
# ======================
class TeacherListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Teacher
    template_name = 'people/teacher_list.html'
    permission_required = 'csms.view_teacher'
    context_object_name = 'teachers'

    def get_queryset(self):
        return super().get_queryset().select_related('user')


class TeacherCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'people/teacher_create.html'
    permission_required = 'csms.add_teacher'
    success_url = reverse_lazy('csms:teacher_list')  # Add namespace
    list_url_name = 'csms:teacher_list'  # Add namespace
    detail_url_name = 'csms:teacher_detail'  # Add namespace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = TeacherUserForm(self.request.POST)
        else:
            context['user_form'] = TeacherUserForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        with transaction.atomic():
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.is_staff = True
                user.save()

                teacher = form.save(commit=False)
                teacher.user = user
                teacher.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'people/teacher_update.html'
    permission_required = 'csms.change_teacher'
    success_url = reverse_lazy('csms:teacher_list')  # Add namespace
    list_url_name = 'csms:teacher_list'  # Add namespace
    detail_url_name = 'csms:teacher_detail'  # Add namespace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = TeacherUserForm(self.request.POST, instance=self.object.user)
        else:
            context['user_form'] = TeacherUserForm(instance=self.object.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        with transaction.atomic():
            if user_form.is_valid():
                user_form.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class TeacherDeleteView(BaseDeleteView):
    model = Teacher
    permission_required = 'csms.delete_teacher'
    template_name = 'crud/delete.html'  # Explicitly set template
    list_url_name = 'csms:teacher_list'  # Make sure this is set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'teacher'  # Set object name for template
        return context


class TeacherDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Teacher
    template_name = 'people/teacher_detail.html'
    permission_required = 'csms.view_teacher'
    context_object_name = 'teacher'


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'people/student_list.html'
    permission_required = 'csms.view_student'
    context_object_name = 'students'

    def get_queryset(self):
        return super().get_queryset().select_related('user', 'course', 'academic_year')


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'people/student_create.html'
    permission_required = 'csms.add_student'
    success_url = reverse_lazy('csms:student_list')  # Add namespace
    list_url_name = 'csms:student_list'  # Add namespace
    detail_url_name = 'csms:student_detail'  # Add namespace


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = StudentUserForm(self.request.POST)
        else:
            context['user_form'] = StudentUserForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        with transaction.atomic():
            if user_form.is_valid():
                user = user_form.save()

                student = form.save(commit=False)
                student.user = user
                student.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'people/student_update.html'
    permission_required = 'csms.change_student'
    success_url = reverse_lazy('csms:student_list')
    list_url_name = 'csms:student_list'
    detail_url_name = 'csms:student_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = StudentUserForm(self.request.POST, instance=self.object.user)
        else:
            context['user_form'] = StudentUserForm(instance=self.object.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        with transaction.atomic():
            if user_form.is_valid():
                user_form.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class StudentDeleteView(BaseDeleteView):
    model = Student
    permission_required = 'csms.delete_student'
    list_url_name = 'csms:student_list'


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    template_name = 'people/student_detail.html'
    permission_required = 'csms.view_student'
    context_object_name = 'student'


class EnrollmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Enrollment
    template_name = 'people/enrollment_list.html'
    permission_required = 'csms.view_enrollment'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'course', 'academic_year', 'semester')


class EnrollmentCreateView(BaseCreateView):
    model = Enrollment
    form_class = EnrollmentForm
    permission_required = 'csms.add_enrollment'
    list_url_name = 'enrollment_list'


class EnrollmentUpdateView(BaseUpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    permission_required = 'csms.change_enrollment'
    list_url_name = 'enrollment_list'


class EnrollmentDeleteView(BaseDeleteView):
    model = Enrollment
    permission_required = 'csms.delete_enrollment'
    list_url_name = 'enrollment_list'


# ======================
# Class Management Views
# ======================
class ClassListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Class
    template_name = 'class/class_list.html'
    permission_required = 'csms.view_class'
    context_object_name = 'csms:classes'

    def get_queryset(self):
        return super().get_queryset().select_related('course', 'academic_year', 'semester', 'teacher')


from django.db.models import Q  # Add this import at the top
from django.forms import inlineformset_factory

ClassSubjectFormSet = inlineformset_factory(
    Class,
    ClassSubject,
    form=ClassSubjectForm,
    extra=1,
    can_delete=True,
    fields=['subject', 'teacher']
)


class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'classes/class_form.html'
    permission_required = 'csms.add_class'

    def get_success_url(self):
        messages.success(self.request, "Class created successfully!")
        return reverse('csms:class_list')

    def form_valid(self, form):
        # Save the class first
        self.object = form.save()

        # Process subject assignments if using formset
        if hasattr(self, 'formset'):
            formset = self.formset(self.request.POST, instance=self.object)
            if formset.is_valid():
                formset.save()

        return super().form_valid(form)


class ClassUpdateView(BaseUpdateView):
    model = Class
    form_class = ClassForm
    permission_required = 'csms.change_class'
    list_url_name = 'csms:class_list'
    detail_url_name = 'csms:class_detail'

    def get_success_url(self):
        return reverse('csms:class_list')  # Redirect to list view after update


class ClassDeleteView(BaseDeleteView):
    model = Class
    permission_required = 'csms.delete_class'
    list_url_name = 'csms:class_list'


class ClassDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Class
    template_name = 'class/class_detail.html'
    permission_required = 'csms.view_class'
    context_object_name = 'csms:class'


class ClassSubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassSubject
    template_name = 'class/class_subject_list.html'
    permission_required = 'csms.view_classsubject'
    context_object_name = 'csms:class_subjects'

    def get_queryset(self):
        return super().get_queryset().select_related('class_obj', 'subject', 'teacher')


class ClassSubjectCreateView(BaseCreateView):
    model = ClassSubject
    form_class = ClassSubjectForm
    permission_required = 'csms.add_classsubject'
    list_url_name = 'csms:class_subject_list'


class ClassSubjectUpdateView(BaseUpdateView):
    model = ClassSubject
    form_class = ClassSubjectForm
    permission_required = 'csms.change_classsubject'
    list_url_name = 'csms:class_subject_list'


class ClassSubjectDeleteView(BaseDeleteView):
    model = ClassSubject
    permission_required = 'csms.delete_classsubject'
    list_url_name = 'csms:class_subject_list'


# ======================
# Exam System Views
# ======================
class ExamTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExamType
    template_name = 'exam/exam_type_list.html'
    permission_required = 'csms.view_examtype'
    context_object_name = 'exam_types'


class ExamTypeCreateView(BaseCreateView):
    model = ExamType
    form_class = ExamTypeForm
    permission_required = 'csms.add_examtype'
    list_url_name = 'exam_type_list'


class ExamTypeUpdateView(BaseUpdateView):
    model = ExamType
    form_class = ExamTypeForm
    permission_required = 'csms.change_examtype'
    list_url_name = 'exam_type_list'


class ExamTypeDeleteView(BaseDeleteView):
    model = ExamType
    permission_required = 'csms.delete_examtype'
    list_url_name = 'exam_type_list'


class ExamListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Exam
    template_name = 'exam/exam_list.html'
    permission_required = 'csms.view_exam'
    context_object_name = 'exams'

    def get_queryset(self):
        return super().get_queryset().select_related('exam_type', 'academic_year', 'semester')


class ExamCreateView(BaseCreateView):
    model = Exam
    form_class = ExamForm
    permission_required = 'csms.add_exam'
    list_url_name = 'exam_list'
    detail_url_name = 'exam_detail'


class ExamUpdateView(BaseUpdateView):
    model = Exam
    form_class = ExamForm
    permission_required = 'csms.change_exam'
    list_url_name = 'exam_list'
    detail_url_name = 'exam_detail'


class ExamDeleteView(BaseDeleteView):
    model = Exam
    permission_required = 'csms.delete_exam'
    list_url_name = 'exam_list'


class ExamDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Exam
    template_name = 'exam/exam_detail.html'
    permission_required = 'csms.view_exam'
    context_object_name = 'exam'


class ExamScheduleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExamSchedule
    template_name = 'exam/exam_schedule_list.html'
    permission_required = 'csms.view_examschedule'
    context_object_name = 'exam_schedules'

    def get_queryset(self):
        return super().get_queryset().select_related('exam', 'subject')


class ExamScheduleCreateView(BaseCreateView):
    model = ExamSchedule
    form_class = ExamScheduleForm
    permission_required = 'csms.add_examschedule'
    list_url_name = 'exam_schedule_list'


class ExamScheduleUpdateView(BaseUpdateView):
    model = ExamSchedule
    form_class = ExamScheduleForm
    permission_required = 'csms.change_examschedule'
    list_url_name = 'exam_schedule_list'


class ExamScheduleDeleteView(BaseDeleteView):
    model = ExamSchedule
    permission_required = 'csms.delete_examschedule'
    list_url_name = 'exam_schedule_list'


class MarkListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mark
    template_name = 'exam/mark_list.html'
    permission_required = 'csms.view_mark'
    context_object_name = 'marks'

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'exam', 'subject', 'paper', 'entered_by')


class MarkCreateView(BaseCreateView):
    model = Mark
    form_class = MarkForm
    permission_required = 'csms.add_mark'
    list_url_name = 'mark_list'


class MarkUpdateView(BaseUpdateView):
    model = Mark
    form_class = MarkForm
    permission_required = 'csms.change_mark'
    list_url_name = 'mark_list'


class MarkDeleteView(BaseDeleteView):
    model = Mark
    permission_required = 'csms.delete_mark'
    list_url_name = 'mark_list'


class GradeAllocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = GradeAllocation
    form_class = GradeAllocationForm
    template_name = 'exam/grade_allocation_form.html'
    permission_required = 'csms.add_gradeallocation'
    detail_url_name = 'mark_list'

    def get_initial(self):
        initial = super().get_initial()
        mark_id = self.kwargs.get('mark_id')
        if mark_id:
            mark = get_object_or_404(Mark, pk=mark_id)
            initial['mark'] = mark

            subject_grading = SubjectGrading.objects.filter(subject=mark.subject).first()
            if subject_grading:
                grade = Grade.objects.filter(
                    grading_scale=subject_grading.grading_scale,
                    min_score__lte=mark.marks,
                    max_score__gte=mark.marks
                ).first()
                if grade:
                    initial['grade'] = grade
                    initial['points'] = grade.points
                    initial['remark'] = grade.remark

        return initial

    def get_success_url(self):
        return reverse_lazy('mark_list')

    def form_valid(self, form):
        mark_id = self.kwargs.get('mark_id')
        if mark_id:
            form.instance.mark = get_object_or_404(Mark, pk=mark_id)
            form.instance.allocated_by = self.request.user.teacher

        return super().form_valid(form)


class GradeAllocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = GradeAllocation
    form_class = GradeAllocationForm
    template_name = 'exam/grade_allocation_form.html'
    permission_required = 'csms.change_gradeallocation'
    detail_url_name = 'mark_list'

    def get_success_url(self):
        return reverse_lazy('mark_list')


class GradeAllocationDeleteView(BaseDeleteView):
    model = GradeAllocation
    permission_required = 'csms.delete_gradeallocation'
    template_name = 'exam/grade_allocation_confirm_delete.html'
    list_url_name = 'mark_list'


class AcademicReportListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AcademicReport
    template_name = 'exam/academic_report_list.html'
    permission_required = 'csms.view_academicreport'
    context_object_name = 'reports'

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'exam', 'overall_grade', 'generated_by')


class AcademicReportCreateView(BaseCreateView):
    model = AcademicReport
    form_class = AcademicReportForm
    permission_required = 'csms.add_academicreport'
    list_url_name = 'academic_report_list'
    detail_url_name = 'academic_report_detail'


class AcademicReportUpdateView(BaseUpdateView):
    model = AcademicReport
    form_class = AcademicReportForm
    permission_required = 'csms.change_academicreport'
    list_url_name = 'academic_report_list'
    detail_url_name = 'academic_report_detail'


class AcademicReportDeleteView(BaseDeleteView):
    model = AcademicReport
    permission_required = 'csms.delete_academicreport'
    list_url_name = 'academic_report_list'


class AcademicReportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AcademicReport
    template_name = 'exam/academic_report_detail.html'
    permission_required = 'csms.view_academicreport'
    context_object_name = 'report'


# ======================
# Financial Views
# ======================
class FeeTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = FeeType
    template_name = 'finance/fee_type_list.html'
    permission_required = 'csms.view_feetype'
    context_object_name = 'fee_types'


class FeeTypeCreateView(BaseCreateView):
    model = FeeType
    form_class = FeeTypeForm
    permission_required = 'csms.add_feetype'
    list_url_name = 'fee_type_list'


class FeeTypeUpdateView(BaseUpdateView):
    model = FeeType
    form_class = FeeTypeForm
    permission_required = 'csms.change_feetype'
    list_url_name = 'fee_type_list'


class FeeTypeDeleteView(BaseDeleteView):
    model = FeeType
    permission_required = 'csms.delete_feetype'
    list_url_name = 'fee_type_list'


class FeeStructureListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'finance/fee_structure_list.html'
    permission_required = 'csms.view_feestructure'
    context_object_name = 'fee_structures'

    def get_queryset(self):
        return super().get_queryset().select_related('course', 'academic_year', 'fee_type')


class FeeStructureCreateView(BaseCreateView):
    model = FeeStructure
    form_class = FeeStructureForm
    permission_required = 'csms.add_feestructure'
    list_url_name = 'fee_structure_list'


class FeeStructureUpdateView(BaseUpdateView):
    model = FeeStructure
    form_class = FeeStructureForm
    permission_required = 'csms.change_feestructure'
    list_url_name = 'fee_structure_list'


class FeeStructureDeleteView(BaseDeleteView):
    model = FeeStructure
    permission_required = 'csms.delete_feestructure'
    list_url_name = 'fee_structure_list'


class StudentFeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StudentFee
    template_name = 'finance/student_fee_list.html'
    permission_required = 'csms.view_studentfee'
    context_object_name = 'student_fees'

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'fee_structure', 'received_by')


class StudentFeeCreateView(BaseCreateView):
    model = StudentFee
    form_class = StudentFeeForm
    permission_required = 'csms.add_studentfee'
    list_url_name = 'student_fee_list'


class StudentFeeUpdateView(BaseUpdateView):
    model = StudentFee
    form_class = StudentFeeForm
    permission_required = 'csms.change_studentfee'
    list_url_name = 'student_fee_list'


class StudentFeeDeleteView(BaseDeleteView):
    model = StudentFee
    permission_required = 'csms.delete_studentfee'
    list_url_name = 'student_fee_list'


# ======================
# Calendar and Attendance Views
# ======================
class AcademicCalendarListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AcademicCalendar
    template_name = 'calendar/academic_calendar_list.html'
    permission_required = 'csms.view_academiccalendar'
    context_object_name = 'events'

    def get_queryset(self):
        return super().get_queryset().select_related('academic_year', 'created_by')


class AcademicCalendarCreateView(BaseCreateView):
    model = AcademicCalendar
    form_class = AcademicCalendarForm
    permission_required = 'csms.add_academiccalendar'
    list_url_name = 'academic_calendar_list'


class AcademicCalendarUpdateView(BaseUpdateView):
    model = AcademicCalendar
    form_class = AcademicCalendarForm
    permission_required = 'csms.change_academiccalendar'
    list_url_name = 'academic_calendar_list'


class AcademicCalendarDeleteView(BaseDeleteView):
    model = AcademicCalendar
    permission_required = 'csms.delete_academiccalendar'
    list_url_name = 'academic_calendar_list'


class AttendanceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    permission_required = 'csms.view_attendance'
    context_object_name = 'attendances'

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'recorded_by')


class AttendanceCreateView(BaseCreateView):
    model = Attendance
    form_class = AttendanceForm
    permission_required = 'csms.add_attendance'
    list_url_name = 'attendance_list'


class AttendanceUpdateView(BaseUpdateView):
    model = Attendance
    form_class = AttendanceForm
    permission_required = 'csms.change_attendance'
    list_url_name = 'attendance_list'


class AttendanceDeleteView(BaseDeleteView):
    model = Attendance
    permission_required = 'csms.delete_attendance'
    list_url_name = 'attendance_list'


# ======================
# Notification Views
# ======================
class NotificationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Notification
    template_name = 'notification/notification_list.html'
    permission_required = 'csms.view_notification'
    context_object_name = 'notifications'

    def get_queryset(self):
        return super().get_queryset().select_related('created_by')


class NotificationCreateView(BaseCreateView):
    model = Notification
    form_class = NotificationForm
    permission_required = 'csms.add_notification'
    list_url_name = 'notification_list'


class NotificationUpdateView(BaseUpdateView):
    model = Notification
    form_class = NotificationForm
    permission_required = 'csms.change_notification'
    list_url_name = 'notification_list'


class NotificationDeleteView(BaseDeleteView):
    model = Notification
    permission_required = 'csms.delete_notification'
    list_url_name = 'notification_list'


# ======================
# Bulk Operations Views
# ======================
class BulkMarkEntryView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'bulk/bulk_mark_entry.html'
    form_class = BulkMarkEntryForm
    permission_required = 'csms.add_mark'
    success_url = reverse_lazy('mark_list')

    def form_valid(self, form):
        try:
            exam = form.cleaned_data['exam']
            subject = form.cleaned_data['subject']
            paper = form.cleaned_data['paper']
            csv_file = form.cleaned_data['marks_file']

            messages.success(self.request, "Marks uploaded successfully")
        except Exception as e:
            messages.error(self.request, f"Error processing file: {str(e)}")

        return super().form_valid(form)


class BulkStudentCreationView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'bulk/bulk_student_creation.html'
    form_class = BulkStudentCreationForm
    permission_required = 'csms.add_student'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        try:
            course = form.cleaned_data['course']
            academic_year = form.cleaned_data['academic_year']
            csv_file = form.cleaned_data['students_file']

            messages.success(self.request, "Students created successfully")
        except Exception as e:
            messages.error(self.request, f"Error processing file: {str(e)}")

        return super().form_valid(form)


# ======================
# Dashboard and Reports
# ======================
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'csms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['student_count'] = Student.objects.count()
            context['teacher_count'] = Teacher.objects.count()
            context['course_count'] = Course.objects.count()
            context['recent_students'] = Student.objects.select_related('user', 'course').order_by('-created_at')[:5]

        return context


class StudentReportView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    template_name = 'reports/student_report.html'
    permission_required = 'csms.view_student'
    context_object_name = 'student'


# ======================
# AJAX Views
# ======================
@login_required
def get_papers_for_subject(request):
    subject_id = request.GET.get('subject_id')
    papers = Paper.objects.filter(subject_id=subject_id).values('id', 'name', 'code')
    return JsonResponse(list(papers), safe=False)


@login_required
def get_students_for_class(request):
    class_id = request.GET.get('class_id')
    students = Student.objects.filter(class_id=class_id).select_related('user').values('id', 'user__first_name',
                                                                                       'user__last_name')
    return JsonResponse(list(students), safe=False)