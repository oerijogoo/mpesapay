from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import (
    School, AcademicYear, Semester, Department, Course, Subject, Paper,
    GradeScale, Grade, SubjectGradeScale, ClassLevel, Class, Student,
    Staff, ClassSubject, Enrollment, Attendance, ExamType, Exam,
    ExamSchedule, ExamResult, SubjectResult, Promotion, ReportComment,
    Notification
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cloudinary.forms import CloudinaryFileField


class SchoolForm(forms.ModelForm):
    logo = CloudinaryFileField(
        required=False,
        options={
            'folder': 'isms/school_logos',
            'tags': ['school_logo'],
            'resource_type': 'image'
        }
    )

    class Meta:
        model = School
        fields = '__all__'
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class AcademicYearForm(forms.ModelForm):
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

        return cleaned_data


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        academic_year = cleaned_data.get('academic_year')

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date")

            if academic_year:
                if start_date < academic_year.start_date or end_date > academic_year.end_date:
                    raise ValidationError("Semester dates must be within the academic year dates")

        return cleaned_data


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SubjectForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subject' in self.fields:
            self.fields['subject'].queryset = Subject.objects.filter(is_active=True)

    def clean_max_weight(self):
        max_weight = self.cleaned_data.get('max_weight')
        subject = self.cleaned_data.get('subject')

        if subject and max_weight:
            existing_papers = subject.papers.exclude(pk=self.instance.pk if self.instance else None)
            total_weight = sum(paper.max_weight for paper in existing_papers) + max_weight

            if total_weight > 100:
                raise ValidationError(
                    f"Adding this paper would exceed 100% total weight. "
                    f"Current total is {total_weight - max_weight}%"
                )

        return max_weight


# Formset for Papers
PaperFormSet = inlineformset_factory(
    Subject, Paper, form=PaperForm,
    fields=['name', 'code', 'max_weight', 'description'],
    extra=1, can_delete=True
)


class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        min_mark = cleaned_data.get('min_mark')
        max_mark = cleaned_data.get('max_mark')

        if min_mark is not None and max_mark is not None and min_mark >= max_mark:
            raise ValidationError("Minimum mark must be less than maximum mark")

        return cleaned_data


class SubjectGradeScaleForm(forms.ModelForm):
    class Meta:
        model = SubjectGradeScale
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subject' in self.fields:
            self.fields['subject'].queryset = Subject.objects.filter(is_active=True)


class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'course' in self.fields:
            self.fields['course'].queryset = Course.objects.filter(is_active=True)
        if 'academic_year' in self.fields:
            self.fields['academic_year'].queryset = AcademicYear.objects.filter(is_current=True)


class UserCreationFormExtended(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class StudentForm(forms.ModelForm):
    photo = CloudinaryFileField(
        required=False,
        options={
            'folder': 'isms/student_photos',
            'tags': ['student_photo'],
            'resource_type': 'image'
        }
    )

    class Meta:
        model = Student
        exclude = ['user']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'current_class' in self.fields:
            self.fields['current_class'].queryset = Class.objects.filter(is_active=True)


class StaffForm(forms.ModelForm):
    photo = CloudinaryFileField(
        required=False,
        options={
            'folder': 'isms/staff_photos',
            'tags': ['staff_photo'],
            'resource_type': 'image'
        }
    )

    class Meta:
        model = Staff
        exclude = ['user']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].queryset = Department.objects.filter(is_active=True)


class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'class_info' in self.fields:
            self.fields['class_info'].queryset = Class.objects.filter(is_active=True)
        if 'subject' in self.fields:
            self.fields['subject'].queryset = Subject.objects.filter(is_active=True)
        if 'teacher' in self.fields:
            self.fields['teacher'].queryset = Staff.objects.filter(is_active=True, is_teaching_staff=True)
        if 'semester' in self.fields:
            self.fields['semester'].queryset = Semester.objects.filter(is_current=True)


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'student' in self.fields:
            self.fields['student'].queryset = Student.objects.filter(is_active=True)
        if 'class_info' in self.fields:
            self.fields['class_info'].queryset = Class.objects.filter(is_active=True)


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'student' in self.fields:
            self.fields['student'].queryset = Student.objects.filter(is_active=True)
        if 'class_subject' in self.fields:
            self.fields['class_subject'].queryset = ClassSubject.objects.filter(is_active=True)


class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        academic_year = cleaned_data.get('academic_year')
        semester = cleaned_data.get('semester')

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date")

            if academic_year:
                if start_date < academic_year.start_date or end_date > academic_year.end_date:
                    raise ValidationError("Exam dates must be within the academic year dates")

            if semester:
                if start_date < semester.start_date or end_date > semester.end_date:
                    raise ValidationError("Exam dates must be within the semester dates")

        return cleaned_data


class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = '__all__'
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'class_subject' in self.fields:
            self.fields['class_subject'].queryset = ClassSubject.objects.filter(is_active=True)
        if 'paper' in self.fields and 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['paper'].queryset = Paper.objects.filter(subject_id=subject_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['paper'].queryset = self.instance.class_subject.subject.papers.all()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time")

        return cleaned_data


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'student' in self.fields:
            self.fields['student'].queryset = Student.objects.filter(is_active=True)
        if 'exam_schedule' in self.fields:
            self.fields['exam_schedule'].queryset = ExamSchedule.objects.all()

    def clean_marks_obtained(self):
        marks_obtained = self.cleaned_data.get('marks_obtained')
        exam_schedule = self.cleaned_data.get('exam_schedule')

        if exam_schedule and marks_obtained:
            if marks_obtained > exam_schedule.max_marks:
                raise ValidationError(
                    f"Marks obtained cannot exceed maximum marks ({exam_schedule.max_marks})"
                )

        return marks_obtained


class SubjectResultForm(forms.ModelForm):
    class Meta:
        model = SubjectResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'student' in self.fields:
            self.fields['student'].queryset = Student.objects.filter(is_active=True)
        if 'class_subject' in self.fields:
            self.fields['class_subject'].queryset = ClassSubject.objects.filter(is_active=True)
        if 'exam' in self.fields:
            self.fields['exam'].queryset = Exam.objects.all()
        if 'grade' in self.fields and 'class_subject' in self.data:
            try:
                class_subject_id = int(self.data.get('class_subject'))
                subject = ClassSubject.objects.get(pk=class_subject_id).subject
                if hasattr(subject, 'grade_scale'):
                    self.fields['grade'].queryset = subject.grade_scale.grade_scale.grades.all()
            except (ValueError, TypeError, ClassSubject.DoesNotExist):
                pass
        elif self.instance.pk:
            if hasattr(self.instance.class_subject.subject, 'grade_scale'):
                self.fields['grade'].queryset = self.instance.class_subject.subject.grade_scale.grade_scale.grades.all()


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'promotion_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'student' in self.fields:
            self.fields['student'].queryset = Student.objects.filter(is_active=True)
        if 'from_class' in self.fields:
            self.fields['from_class'].queryset = Class.objects.filter(is_active=True)
        if 'to_class' in self.fields:
            self.fields['to_class'].queryset = Class.objects.filter(is_active=True)
        if 'academic_year' in self.fields:
            self.fields['academic_year'].queryset = AcademicYear.objects.filter(is_current=True)

    def clean(self):
        cleaned_data = super().clean()
        from_class = cleaned_data.get('from_class')
        to_class = cleaned_data.get('to_class')

        if from_class and to_class and from_class == to_class:
            raise ValidationError("From class and To class cannot be the same")

        return cleaned_data


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'class_info' in self.fields:
            self.fields['class_info'].queryset = Class.objects.filter(is_active=True)
        if 'student' in self.fields:
            self.fields['student'].queryset = Student.objects.filter(is_active=True)
        if 'semester' in self.fields:
            self.fields['semester'].queryset = Semester.objects.filter(is_active=True)
        if 'created_by' in self.fields:
            self.fields['created_by'].queryset = Staff.objects.filter(is_active=True)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }


# Custom form for bulk actions
class BulkStudentEnrollmentForm(forms.Form):
    class_info = forms.ModelChoiceField(queryset=Class.objects.filter(is_active=True))
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={'size': 20}))
    enrollment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class BulkAttendanceForm(forms.Form):
    class_subject = forms.ModelChoiceField(queryset=ClassSubject.objects.filter(is_active=True))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=Attendance.STATUS_CHOICES, initial='P')
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'class_subject' in self.data:
            try:
                class_subject_id = int(self.data.get('class_subject'))
                class_info = ClassSubject.objects.get(pk=class_subject_id).class_info
                self.fields['students'].queryset = class_info.enrollment_set.filter(
                    is_active=True
                ).values_list('student', flat=True)
            except (ValueError, TypeError, ClassSubject.DoesNotExist):
                pass