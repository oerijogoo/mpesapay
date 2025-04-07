# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import (
    SchoolSettings, AcademicYear, Semester, AcademicLevel, Course,
    Subject, Paper, CourseSubject, GradingScale, Grade, SubjectGrading,
    Teacher, Student, Enrollment, Class, ClassSubject, ExamType, Exam,
    ExamSchedule, Mark, GradeAllocation, AcademicReport, FeeType,
    FeeStructure, StudentFee, AcademicCalendar, Attendance, Notification
)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q  # Add this import

User = get_user_model()



# Helper forms and mixins
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# User Management Forms
class UserCreateForm(UserCreationForm, BootstrapFormMixin):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# School Configuration Forms
class SchoolSettingsForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = SchoolSettings
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


# Academic Structure Forms
class AcademicYearForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = AcademicYear
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be after start date")


class SemesterForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Semester
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AcademicLevelForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = AcademicLevel
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


# Course and Subject Forms
class CourseForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SubjectForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class PaperForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Paper
        fields = ['name', 'code', 'weight', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }


# Formset for adding papers when creating/editing a subject
PaperFormSet = inlineformset_factory(
    Subject, Paper, form=PaperForm,
    extra=1, can_delete=True, can_order=False
)


class CourseSubjectForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = CourseSubject
        fields = '__all__'


# Grading System Forms
class GradingScaleForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = GradingScale
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class GradeForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Grade
        fields = '__all__'
        widgets = {
            'min_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'max_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'points': forms.NumberInput(attrs={'step': '0.1'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        min_score = cleaned_data.get('min_score')
        max_score = cleaned_data.get('max_score')

        if min_score and max_score and min_score >= max_score:
            raise ValidationError("Minimum score must be less than maximum score")


class SubjectGradingForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = SubjectGrading
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


# People Management Forms
class TeacherForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class TeacherUserForm(UserCreateForm):
    class Meta(UserCreateForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class StudentForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'admission_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class StudentUserForm(UserCreateForm):
    class Meta(UserCreateForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class EnrollmentForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Enrollment
        fields = '__all__'
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Class Management Forms
class ClassForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Class
        fields = ['name', 'course', 'academic_year', 'semester', 'teacher', 'is_active']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order teacher choices by last name
        self.fields['teacher'].queryset = Teacher.objects.all().order_by('user__last_name')


class ClassSubjectForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = ClassSubject
        fields = '__all__'
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'class_obj': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'teacher' in self.fields:
            self.fields['teacher'].queryset = Teacher.objects.all().order_by('user__last_name')  # Changed here too

    def clean(self):
        cleaned_data = super().clean()
        class_obj = cleaned_data.get('class_obj')
        subject = cleaned_data.get('subject')

        # Check for existing class-subject combination
        if class_obj and subject:
            existing = ClassSubject.objects.filter(
                class_obj=class_obj,
                subject=subject
            ).exclude(pk=self.instance.pk if self.instance else None)

            if existing.exists():
                raise ValidationError(
                    "This subject is already assigned to this class"
                )
        return cleaned_data


# Exam System Forms
class ExamTypeForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = ExamType
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }


class ExamForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ExamScheduleForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = ExamSchedule
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class MarkForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Mark
        fields = ['exam', 'subject', 'paper', 'marks', 'comment']
        widgets = {
            'marks': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically filter papers based on selected subject
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['paper'].queryset = Paper.objects.filter(subject_id=subject_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['paper'].queryset = self.instance.subject.papers.all()
        else:
            self.fields['paper'].queryset = Paper.objects.none()


class GradeAllocationForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = GradeAllocation
        fields = ['grade', 'remark']


class AcademicReportForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = AcademicReport
        fields = ['remarks', 'is_published']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }


# Financial Forms
class FeeTypeForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = FeeType
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class FeeStructureForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = FeeStructure
        fields = '__all__'
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StudentFeeForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = StudentFee
        fields = ['fee_structure', 'amount_paid', 'payment_date', 'payment_method', 'transaction_reference', 'remarks']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'amount_paid': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_amount_paid(self):
        amount_paid = self.cleaned_data.get('amount_paid')
        fee_structure = self.cleaned_data.get('fee_structure')

        if fee_structure and amount_paid > fee_structure.amount:
            raise ValidationError("Amount paid cannot exceed the fee amount")
        return amount_paid


# Calendar and Attendance Forms
class AcademicCalendarForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = AcademicCalendar
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AttendanceForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


# Notification Form
class NotificationForm(forms.ModelForm, BootstrapFormMixin):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=True
    )

    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'recipients']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


# Bulk Operations Forms
class BulkMarkEntryForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exam.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    paper = forms.ModelChoiceField(queryset=Paper.objects.none(), required=False)
    marks_file = forms.FileField(label='Marks CSV File')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['paper'].queryset = Paper.objects.filter(subject_id=subject_id)
            except (ValueError, TypeError):
                pass


class BulkStudentCreationForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    academic_year = forms.ModelChoiceField(queryset=AcademicYear.objects.all())
    students_file = forms.FileField(label='Students CSV File')