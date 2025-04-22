from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Q
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .models import (
    School, AcademicYear, Semester, Department, Course, Subject, Paper,
    GradeScale, Grade, SubjectGradeScale, ClassLevel, Class, Student,
    Staff, ClassSubject, Enrollment, Attendance, ExamType, Exam,
    ExamSchedule, ExamResult, SubjectResult, Promotion, ReportComment,
    Notification
)
from .forms import (
    SchoolForm, AcademicYearForm, SemesterForm, DepartmentForm, CourseForm,
    SubjectForm, PaperForm, GradeScaleForm, GradeForm, SubjectGradeScaleForm,
    ClassLevelForm, ClassForm, StudentForm, StaffForm, ClassSubjectForm,
    EnrollmentForm, AttendanceForm, ExamTypeForm, ExamForm, ExamScheduleForm,
    ExamResultForm, SubjectResultForm, PromotionForm, ReportCommentForm,
    NotificationForm, BulkStudentEnrollmentForm, BulkAttendanceForm,
    UserCreationFormExtended, PaperFormSet
)
from django.contrib.auth.models import Group, User


class SchoolView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = School
    form_class = SchoolForm
    template_name = 'isms/school_form.html'
    permission_required = 'isms.change_school'
    success_url = reverse_lazy('school_view')

    def get_object(self):
        # Assuming only one school exists
        return School.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'School Information'
        return context


# Academic Year Views
class AcademicYearListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AcademicYear
    template_name = 'isms/academic_year_list.html'
    permission_required = 'isms.view_academicyear'
    context_object_name = 'academic_years'


class AcademicYearCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'isms/academic_year_form.html'
    permission_required = 'isms.add_academicyear'
    success_url = reverse_lazy('academic_year_list')


class AcademicYearUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = 'isms/academic_year_form.html'
    permission_required = 'isms.change_academicyear'
    success_url = reverse_lazy('academic_year_list')


class AcademicYearDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AcademicYear
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_academicyear'
    success_url = reverse_lazy('academic_year_list')


# Semester Views
class SemesterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Semester
    template_name = 'isms/semester_list.html'
    permission_required = 'isms.view_semester'
    context_object_name = 'semesters'

    def get_queryset(self):
        return Semester.objects.select_related('academic_year')


class SemesterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'isms/semester_form.html'
    permission_required = 'isms.add_semester'
    success_url = reverse_lazy('semester_list')


class SemesterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'isms/semester_form.html'
    permission_required = 'isms.change_semester'
    success_url = reverse_lazy('semester_list')


class SemesterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Semester
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_semester'
    success_url = reverse_lazy('semester_list')


# Department Views
class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Department
    template_name = 'isms/department_list.html'
    permission_required = 'isms.view_department'
    context_object_name = 'departments'


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'isms/department_form.html'
    permission_required = 'isms.add_department'
    success_url = reverse_lazy('department_list')


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'isms/department_form.html'
    permission_required = 'isms.change_department'
    success_url = reverse_lazy('department_list')


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_department'
    success_url = reverse_lazy('department_list')


# Course Views
class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    template_name = 'isms/course_list.html'
    permission_required = 'isms.view_course'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.select_related('department')


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'isms/course_form.html'
    permission_required = 'isms.add_course'
    success_url = reverse_lazy('course_list')


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'isms/course_form.html'
    permission_required = 'isms.change_course'
    success_url = reverse_lazy('course_list')


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_course'
    success_url = reverse_lazy('course_list')


# Subject Views
class SubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Subject
    template_name = 'isms/subject_list.html'
    permission_required = 'isms.view_subject'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.prefetch_related('courses')


class SubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'isms/subject_form.html'
    permission_required = 'isms.add_subject'
    success_url = reverse_lazy('subject_list')

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

        if paper_formset.is_valid():
            self.object = form.save()
            paper_formset.instance = self.object
            paper_formset.save()

            # Validate total weight
            total_weight = self.object.papers.aggregate(Sum('max_weight'))['max_weight__sum'] or 0
            if total_weight > 100:
                form.add_error(None, "Total weight of all papers cannot exceed 100%")
                return self.form_invalid(form)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class SubjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'isms/subject_form.html'
    permission_required = 'isms.change_subject'
    success_url = reverse_lazy('subject_list')

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

        if paper_formset.is_valid():
            self.object = form.save()
            paper_formset.instance = self.object
            paper_formset.save()

            # Validate total weight
            total_weight = self.object.papers.aggregate(Sum('max_weight'))['max_weight__sum'] or 0
            if total_weight > 100:
                form.add_error(None, "Total weight of all papers cannot exceed 100%")
                return self.form_invalid(form)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class SubjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Subject
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_subject'
    success_url = reverse_lazy('subject_list')


# Paper Views
class PaperUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Paper
    form_class = PaperForm
    template_name = 'isms/paper_form.html'
    permission_required = 'isms.change_paper'

    def get_success_url(self):
        return reverse_lazy('subject_update', kwargs={'pk': self.object.subject.pk})


class PaperDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Paper
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_paper'

    def get_success_url(self):
        return reverse_lazy('subject_update', kwargs={'pk': self.object.subject.pk})


# Grade Scale Views
class GradeScaleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = GradeScale
    template_name = 'isms/grade_scale_list.html'
    permission_required = 'isms.view_gradescale'
    context_object_name = 'grade_scales'


class GradeScaleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = GradeScale
    form_class = GradeScaleForm
    template_name = 'isms/grade_scale_form.html'
    permission_required = 'isms.add_gradescale'
    success_url = reverse_lazy('grade_scale_list')


class GradeScaleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = GradeScale
    form_class = GradeScaleForm
    template_name = 'isms/grade_scale_form.html'
    permission_required = 'isms.change_gradescale'
    success_url = reverse_lazy('grade_scale_list')


class GradeScaleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = GradeScale
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_gradescale'
    success_url = reverse_lazy('grade_scale_list')


# Grade Views
class GradeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Grade
    template_name = 'isms/grade_list.html'
    permission_required = 'isms.view_grade'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.select_related('scale')


class GradeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'isms/grade_form.html'
    permission_required = 'isms.add_grade'
    success_url = reverse_lazy('grade_list')


class GradeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'isms/grade_form.html'
    permission_required = 'isms.change_grade'
    success_url = reverse_lazy('grade_list')


class GradeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Grade
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_grade'
    success_url = reverse_lazy('grade_list')


# Subject Grade Scale Views
class SubjectGradeScaleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SubjectGradeScale
    form_class = SubjectGradeScaleForm
    template_name = 'isms/subject_grade_scale_form.html'
    permission_required = 'isms.add_subjectgradescale'
    success_url = reverse_lazy('subject_list')


class SubjectGradeScaleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SubjectGradeScale
    form_class = SubjectGradeScaleForm
    template_name = 'isms/subject_grade_scale_form.html'
    permission_required = 'isms.change_subjectgradescale'
    success_url = reverse_lazy('subject_list')


class SubjectGradeScaleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SubjectGradeScale
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_subjectgradescale'
    success_url = reverse_lazy('subject_list')


# Class Level Views
class ClassLevelListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassLevel
    template_name = 'isms/class_level_list.html'
    permission_required = 'isms.view_classlevel'
    context_object_name = 'class_levels'


class ClassLevelCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'isms/class_level_form.html'
    permission_required = 'isms.add_classlevel'
    success_url = reverse_lazy('class_level_list')


class ClassLevelUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'isms/class_level_form.html'
    permission_required = 'isms.change_classlevel'
    success_url = reverse_lazy('class_level_list')


class ClassLevelDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ClassLevel
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_classlevel'
    success_url = reverse_lazy('class_level_list')


# Class Views
class ClassListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Class
    template_name = 'isms/class_list.html'
    permission_required = 'isms.view_class'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.select_related('course', 'level', 'academic_year', 'class_teacher')


class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'isms/class_form.html'
    permission_required = 'isms.add_class'
    success_url = reverse_lazy('class_list')


class ClassUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'isms/class_form.html'
    permission_required = 'isms.change_class'
    success_url = reverse_lazy('class_list')


class ClassDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Class
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_class'
    success_url = reverse_lazy('class_list')


# Student Views
class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'isms/student_list.html'
    permission_required = 'isms.view_student'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(admission_number__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        return queryset.select_related('current_class')


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'isms/student_form.html'
    permission_required = 'isms.add_student'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        # Step 1: Create user first
        username = form.cleaned_data['admission_number']
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data.get('email', '')
        )

        # Step 2: Assign user to the student instance
        form.instance.user = user

        # Step 3: Save the student with the user now set
        response = super().form_valid(form)

        # Step 4: Add user to student group
        student_group, _ = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)

        return response



class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'isms/student_form.html'
    permission_required = 'isms.change_student'
    success_url = reverse_lazy('student_list')


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_student'
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        if student.user:
            student.user.delete()
        return super().delete(request, *args, **kwargs)


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    template_name = 'isms/student_detail.html'
    permission_required = 'isms.view_student'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()

        # Get current enrollment
        if student.current_class:
            context['enrollment'] = Enrollment.objects.filter(
                student=student,
                class_info=student.current_class
            ).first()

        # Get academic history
        context['enrollments'] = Enrollment.objects.filter(student=student).select_related('class_info')

        # Get results
        context['results'] = SubjectResult.objects.filter(student=student).select_related(
            'class_subject', 'exam', 'grade'
        )

        return context


# Staff Views
class StaffListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'isms/staff_list.html'
    permission_required = 'isms.view_staff'
    context_object_name = 'staff_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(staff_id__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        return queryset.select_related('department')


class StaffCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'isms/staff_form.html'
    permission_required = 'isms.add_staff'
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        # Step 1: Create the user first
        username = form.cleaned_data['staff_id']
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
        )

        # Step 2: Assign the user to the staff before saving
        form.instance.user = user

        # Step 3: Save the staff (now it won't error)
        response = super().form_valid(form)

        # Step 4: Add user to appropriate group
        if form.cleaned_data['is_teaching_staff']:
            staff_group, _ = Group.objects.get_or_create(name='Teacher')
        else:
            staff_group, _ = Group.objects.get_or_create(name='Non-Teaching Staff')

        user.groups.add(staff_group)

        return response


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'isms/staff_form.html'
    permission_required = 'isms.change_staff'
    success_url = reverse_lazy('staff_list')


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Staff
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_staff'
    success_url = reverse_lazy('staff_list')

    def delete(self, request, *args, **kwargs):
        staff = self.get_object()
        if staff.user:
            staff.user.delete()
        return super().delete(request, *args, **kwargs)


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Staff
    template_name = 'isms/staff_detail.html'
    permission_required = 'isms.view_staff'
    context_object_name = 'staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.get_object()

        if staff.is_teaching_staff:
            context['class_subjects'] = ClassSubject.objects.filter(teacher=staff).select_related(
                'class_info', 'subject', 'semester'
            )

        return context


# Class Subject Views
class ClassSubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassSubject
    template_name = 'isms/class_subject_list.html'
    permission_required = 'isms.view_classsubject'
    context_object_name = 'class_subjects'

    def get_queryset(self):
        return ClassSubject.objects.select_related('class_info', 'subject', 'teacher', 'semester')


class ClassSubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ClassSubject
    form_class = ClassSubjectForm
    template_name = 'isms/class_subject_form.html'
    permission_required = 'isms.add_classsubject'
    success_url = reverse_lazy('class_subject_list')


class ClassSubjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ClassSubject
    form_class = ClassSubjectForm
    template_name = 'isms/class_subject_form.html'
    permission_required = 'isms.change_classsubject'
    success_url = reverse_lazy('class_subject_list')


class ClassSubjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ClassSubject
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_classsubject'
    success_url = reverse_lazy('class_subject_list')


# Enrollment Views
class EnrollmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Enrollment
    template_name = 'isms/enrollment_list.html'
    permission_required = 'isms.view_enrollment'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.select_related('student', 'class_info')


class EnrollmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'isms/enrollment_form.html'
    permission_required = 'isms.add_enrollment'
    success_url = reverse_lazy('enrollment_list')


class EnrollmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'isms/enrollment_form.html'
    permission_required = 'isms.change_enrollment'
    success_url = reverse_lazy('enrollment_list')


class EnrollmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_enrollment'
    success_url = reverse_lazy('enrollment_list')


# Bulk Enrollment View
class BulkEnrollmentView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = BulkStudentEnrollmentForm
    template_name = 'isms/bulk_enrollment_form.html'
    permission_required = 'isms.add_enrollment'
    success_url = reverse_lazy('enrollment_list')

    def form_valid(self, form):
        class_info = form.cleaned_data['class_info']
        students = form.cleaned_data['students']
        enrollment_date = form.cleaned_data['enrollment_date']

        enrollments_created = 0
        for student in students:
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                class_info=class_info,
                defaults={'enrollment_date': enrollment_date}
            )
            if created:
                enrollments_created += 1
                # Update student's current class if needed
                if not student.current_class or student.current_class.level.pk < class_info.level.pk:
                    student.current_class = class_info
                    student.save()

        messages.success(
            self.request,
            f'Successfully enrolled {enrollments_created} students in {class_info.name}'
        )
        return super().form_valid(form)


# Attendance Views
class AttendanceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Attendance
    template_name = 'isms/attendance_list.html'
    permission_required = 'isms.view_attendance'
    context_object_name = 'attendances'

    def get_queryset(self):
        queryset = Attendance.objects.select_related('student', 'class_subject')

        # Filter by class if provided
        class_id = self.request.GET.get('class_id')
        if class_id:
            queryset = queryset.filter(class_subject__class_info_id=class_id)

        # Filter by date range if provided
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])

        return queryset


class AttendanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'isms/attendance_form.html'
    permission_required = 'isms.add_attendance'
    success_url = reverse_lazy('attendance_list')


class AttendanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'isms/attendance_form.html'
    permission_required = 'isms.change_attendance'
    success_url = reverse_lazy('attendance_list')


class AttendanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_attendance'
    success_url = reverse_lazy('attendance_list')


# Bulk Attendance View
class BulkAttendanceView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = BulkAttendanceForm
    template_name = 'isms/bulk_attendance_form.html'
    permission_required = 'isms.add_attendance'
    success_url = reverse_lazy('attendance_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and 'class_subject_id' in self.request.GET:
            kwargs['initial'] = {
                'class_subject': self.request.GET.get('class_subject_id')
            }
        return kwargs

    def form_valid(self, form):
        class_subject = form.cleaned_data['class_subject']
        date = form.cleaned_data['date']
        status = form.cleaned_data['status']
        students = form.cleaned_data['students']

        attendances_created = 0
        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                class_subject=class_subject,
                date=date,
                defaults={'status': status}
            )
            if created:
                attendances_created += 1

        messages.success(
            self.request,
            f'Successfully recorded attendance for {attendances_created} students'
        )
        return super().form_valid(form)


# Exam Type Views
class ExamTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExamType
    template_name = 'isms/exam_type_list.html'
    permission_required = 'isms.view_examtype'
    context_object_name = 'exam_types'


class ExamTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'isms/exam_type_form.html'
    permission_required = 'isms.add_examtype'
    success_url = reverse_lazy('exam_type_list')


class ExamTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'isms/exam_type_form.html'
    permission_required = 'isms.change_examtype'
    success_url = reverse_lazy('exam_type_list')


class ExamTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExamType
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_examtype'
    success_url = reverse_lazy('exam_type_list')


# Exam Views
class ExamListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Exam
    template_name = 'isms/exam_list.html'
    permission_required = 'isms.view_exam'
    context_object_name = 'exams'

    def get_queryset(self):
        return Exam.objects.select_related('exam_type', 'academic_year', 'semester')


class ExamCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'isms/exam_form.html'
    permission_required = 'isms.add_exam'
    success_url = reverse_lazy('exam_list')


class ExamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'isms/exam_form.html'
    permission_required = 'isms.change_exam'
    success_url = reverse_lazy('exam_list')


class ExamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Exam
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_exam'
    success_url = reverse_lazy('exam_list')


# Exam Schedule Views
class ExamScheduleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExamSchedule
    template_name = 'isms/exam_schedule_list.html'
    permission_required = 'isms.view_examschedule'
    context_object_name = 'exam_schedules'

    def get_queryset(self):
        queryset = ExamSchedule.objects.select_related(
            'exam', 'class_subject', 'paper', 'class_subject__class_info'
        )

        exam_id = self.request.GET.get('exam_id')
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)

        return queryset


class ExamScheduleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExamSchedule
    form_class = ExamScheduleForm
    template_name = 'isms/exam_schedule_form.html'
    permission_required = 'isms.add_examschedule'
    success_url = reverse_lazy('exam_schedule_list')


class ExamScheduleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ExamSchedule
    form_class = ExamScheduleForm
    template_name = 'isms/exam_schedule_form.html'
    permission_required = 'isms.change_examschedule'
    success_url = reverse_lazy('exam_schedule_list')


class ExamScheduleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExamSchedule
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_examschedule'
    success_url = reverse_lazy('exam_schedule_list')


# Exam Result Views
class ExamResultListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExamResult
    template_name = 'isms/exam_result_list.html'
    permission_required = 'isms.view_examresult'
    context_object_name = 'exam_results'

    def get_queryset(self):
        queryset = ExamResult.objects.select_related(
            'exam_schedule', 'student', 'exam_schedule__class_subject'
        )

        exam_schedule_id = self.request.GET.get('exam_schedule_id')
        if exam_schedule_id:
            queryset = queryset.filter(exam_schedule_id=exam_schedule_id)

        return queryset


class ExamResultCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExamResult
    form_class = ExamResultForm
    template_name = 'isms/exam_result_form.html'
    permission_required = 'isms.add_examresult'
    success_url = reverse_lazy('exam_result_list')


class ExamResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ExamResult
    form_class = ExamResultForm
    template_name = 'isms/exam_result_form.html'
    permission_required = 'isms.change_examresult'
    success_url = reverse_lazy('exam_result_list')


class ExamResultDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExamResult
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_examresult'
    success_url = reverse_lazy('exam_result_list')


# Subject Result Views
class SubjectResultListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SubjectResult
    template_name = 'isms/subject_result_list.html'
    permission_required = 'isms.view_subjectresult'
    context_object_name = 'subject_results'

    def get_queryset(self):
        queryset = SubjectResult.objects.select_related(
            'student', 'class_subject', 'exam', 'grade'
        )

        class_subject_id = self.request.GET.get('class_subject_id')
        exam_id = self.request.GET.get('exam_id')

        if class_subject_id:
            queryset = queryset.filter(class_subject_id=class_subject_id)
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)

        return queryset


class SubjectResultCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SubjectResult
    form_class = SubjectResultForm
    template_name = 'isms/subject_result_form.html'
    permission_required = 'isms.add_subjectresult'
    success_url = reverse_lazy('subject_result_list')


class SubjectResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SubjectResult
    form_class = SubjectResultForm
    template_name = 'isms/subject_result_form.html'
    permission_required = 'isms.change_subjectresult'
    success_url = reverse_lazy('subject_result_list')


class SubjectResultDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SubjectResult
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_subjectresult'
    success_url = reverse_lazy('subject_result_list')


# Promotion Views
class PromotionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Promotion
    template_name = 'isms/promotion_list.html'
    permission_required = 'isms.view_promotion'
    context_object_name = 'promotions'

    def get_queryset(self):
        return Promotion.objects.select_related(
            'student', 'from_class', 'to_class', 'academic_year'
        )


class PromotionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'isms/promotion_form.html'
    permission_required = 'isms.add_promotion'
    success_url = reverse_lazy('promotion_list')


class PromotionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'isms/promotion_form.html'
    permission_required = 'isms.change_promotion'
    success_url = reverse_lazy('promotion_list')


class PromotionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Promotion
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_promotion'
    success_url = reverse_lazy('promotion_list')


# Report Comment Views
class ReportCommentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ReportComment
    template_name = 'isms/report_comment_list.html'
    permission_required = 'isms.view_reportcomment'
    context_object_name = 'report_comments'

    def get_queryset(self):
        queryset = ReportComment.objects.select_related(
            'class_info', 'student', 'semester', 'created_by'
        )

        student_id = self.request.GET.get('student_id')
        semester_id = self.request.GET.get('semester_id')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if semester_id:
            queryset = queryset.filter(semester_id=semester_id)

        return queryset


class ReportCommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ReportComment
    form_class = ReportCommentForm
    template_name = 'isms/report_comment_form.html'
    permission_required = 'isms.add_reportcomment'
    success_url = reverse_lazy('report_comment_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.staff
        return super().form_valid(form)


class ReportCommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ReportComment
    form_class = ReportCommentForm
    template_name = 'isms/report_comment_form.html'
    permission_required = 'isms.change_reportcomment'
    success_url = reverse_lazy('report_comment_list')


class ReportCommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ReportComment
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_reportcomment'
    success_url = reverse_lazy('report_comment_list')


# Notification Views
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'isms/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')


class NotificationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'isms/notification_form.html'
    permission_required = 'isms.add_notification'
    success_url = reverse_lazy('notification_list')


class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = 'isms/notification_detail.html'
    context_object_name = 'notification'

    def get(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient != request.user:
            raise PermissionDenied
        notification.is_read = True
        notification.save()
        return super().get(request, *args, **kwargs)


class NotificationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Notification
    template_name = 'isms/confirm_delete.html'
    permission_required = 'isms.delete_notification'
    success_url = reverse_lazy('notification_list')


# AJAX Views
def get_papers_for_subject(request):
    subject_id = request.GET.get('subject_id')
    papers = Paper.objects.filter(subject_id=subject_id).values('id', 'name', 'code')
    return JsonResponse(list(papers), safe=False)


def get_students_for_class(request):
    class_id = request.GET.get('class_id')
    enrollments = Enrollment.objects.filter(
        class_info_id=class_id,
        is_active=True
    ).select_related('student')

    students = [{
        'id': e.student.id,
        'name': e.student.get_full_name(),
        'admission_number': e.student.admission_number
    } for e in enrollments]

    return JsonResponse(students, safe=False)


def get_subjects_for_class(request):
    class_id = request.GET.get('class_id')
    class_subjects = ClassSubject.objects.filter(
        class_info_id=class_id,
        is_active=True
    ).select_related('subject')

    subjects = [{
        'id': cs.subject.id,
        'name': cs.subject.name,
        'code': cs.subject.code
    } for cs in class_subjects]

    return JsonResponse(subjects, safe=False)


# Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'isms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self.request.user, 'student'):
            student = self.request.user.student
            context['student'] = student
            context['current_class'] = student.current_class
            context['recent_results'] = SubjectResult.objects.filter(
                student=student
            ).select_related('class_subject', 'exam').order_by('-exam__start_date')[:5]
            context['recent_attendances'] = Attendance.objects.filter(
                student=student
            ).select_related('class_subject').order_by('-date')[:5]

        elif hasattr(self.request.user, 'staff'):
            staff = self.request.user.staff
            context['staff'] = staff

            if staff.is_teaching_staff:
                context['class_subjects'] = ClassSubject.objects.filter(
                    teacher=staff,
                    is_active=True
                ).select_related('class_info', 'subject')[:5]

                context['recent_exams'] = ExamSchedule.objects.filter(
                    class_subject__teacher=staff
                ).select_related('exam', 'class_subject').order_by('-exam_date')[:5]

        # Admin dashboard
        else:
            context['total_students'] = Student.objects.filter(is_active=True).count()
            context['total_staff'] = Staff.objects.filter(is_active=True).count()
            context['current_academic_year'] = AcademicYear.objects.filter(is_current=True).first()
            context['current_semester'] = Semester.objects.filter(is_current=True).first()
            context['recent_enrollments'] = Enrollment.objects.select_related(
                'student', 'class_info'
            ).order_by('-enrollment_date')[:5]

        return context



class PaperCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = 'isms/paper_form.html'
    permission_required = 'isms.add_paper'

    def get_initial(self):
        initial = super().get_initial()
        subject_id = self.kwargs.get('subject_pk')
        if subject_id:
            initial['subject'] = get_object_or_404(Subject, pk=subject_id)
        return initial

    def get_success_url(self):
        return reverse('subject_update', kwargs={'pk': self.object.subject.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = self.kwargs.get('subject_pk')
        if subject_id:
            context['subject'] = get_object_or_404(Subject, pk=subject_id)
        return context


class NotificationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notification_form.html'
    permission_required = 'isms.change_notification'
    success_url = reverse_lazy('notification_list')

    def get_queryset(self):
        # Only allow updating notifications for the current user
        return Notification.objects.filter(recipient=self.request.user)



from django.http import JsonResponse

def get_subject_for_class_subject(request):
    class_subject_id = request.GET.get('class_subject_id')
    if class_subject_id:
        try:
            class_subject = ClassSubject.objects.get(pk=class_subject_id)
            return JsonResponse({
                'subject_id': class_subject.subject.id,
                'subject_name': class_subject.subject.name
            })
        except ClassSubject.DoesNotExist:
            pass
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_grade_scale_for_subject(request):
    subject_id = request.GET.get('subject_id')
    if subject_id:
        try:
            subject = Subject.objects.get(pk=subject_id)
            if hasattr(subject, 'grade_scale'):
                grades = subject.grade_scale.grade_scale.grades.all().values(
                    'id', 'name', 'min_mark', 'max_mark'
                )
                return JsonResponse({
                    'grades': list(grades)
                })
        except Subject.DoesNotExist:
            pass
    return JsonResponse({'error': 'Invalid request'}, status=400)