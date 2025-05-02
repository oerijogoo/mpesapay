from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Div
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-md-6'),
                Column('user_type', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('phone', css_class='col-md-6'),
                Column('profile_picture', css_class='col-md-6'),
            ),
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            Submit('submit', 'Create Account', css_class='btn-primary')
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone', 'profile_picture', 'is_active')


class SchoolConfigForm(forms.ModelForm):
    class Meta:
        model = SchoolConfig
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'motto': forms.TextInput(attrs={'placeholder': 'School motto or slogan'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'School Information',
                Row(
                    Column('name', css_class='col-md-6'),
                    Column('motto', css_class='col-md-6'),
                ),
                Row(
                    Column('logo', css_class='col-md-6'),
                    Column('current_academic_year', css_class='col-md-6'),
                ),
                'address',
                Row(
                    Column('phone', css_class='col-md-4'),
                    Column('email', css_class='col-md-4'),
                    Column('website', css_class='col-md-4'),
                ),
            ),
            Fieldset(
                'ID Prefixes',
                Row(
                    Column('student_id_prefix', css_class='col-md-4'),
                    Column('teacher_id_prefix', css_class='col-md-4'),
                    Column('staff_id_prefix', css_class='col-md-4'),
                ),
            ),
            Submit('submit', 'Save Configuration', css_class='btn-primary')
        )


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be after start date")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('is_current', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Academic Year', css_class='btn-primary')
        )


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        academic_year = cleaned_data.get('academic_year')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be after start date")

        if academic_year and start_date and end_date:
            if start_date < academic_year.start_date or end_date > academic_year.end_date:
                raise ValidationError("Semester dates must be within academic year dates")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('academic_year', css_class='col-md-6'),
                Column('name', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Row(
                Column('is_current', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Semester', css_class='btn-primary')
        )


class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('code', css_class='col-md-6'),
            ),
            Row(
                Column('order', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Class Level', css_class='btn-primary')
        )


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('class_level', css_class='col-md-6'),
                Column('name', css_class='col-md-6'),
            ),
            Row(
                Column('code', css_class='col-md-6'),
                Column('capacity', css_class='col-md-6'),
            ),
            Row(
                Column('class_teacher', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Class', css_class='btn-primary')
        )


class SubjectForm(forms.ModelForm):
    class_levels = forms.ModelMultipleChoiceField(
        queryset=ClassLevel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Subject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('code', css_class='col-md-6'),
            ),
            Row(
                Column('is_core', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            'description',
            'class_levels',
            Submit('submit', 'Save Subject', css_class='btn-primary')
        )


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['name', 'code', 'weight']
        widgets = {
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 100})
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is None:
            raise forms.ValidationError("Weight is required")
        if not (1 <= weight <= 100):
            raise forms.ValidationError("Weight must be between 1 and 100")
        return weight


class GradingSystemForm(forms.ModelForm):
    class Meta:
        model = GradingSystem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('is_default', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Grading System', css_class='btn-primary')
        )


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        min_score = cleaned_data.get('min_score')
        max_score = cleaned_data.get('max_score')

        if min_score and max_score and min_score >= max_score:
            raise ValidationError("Minimum score must be less than maximum score")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('grading_system', css_class='col-md-6'),
                Column('name', css_class='col-md-6'),
            ),
            Row(
                Column('min_score', css_class='col-md-6'),
                Column('max_score', css_class='col-md-6'),
            ),
            Row(
                Column('points', css_class='col-md-6'),
                Column('remark', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Grade', css_class='btn-primary')
        )


class SubjectGradingForm(forms.ModelForm):
    class Meta:
        model = SubjectGrading
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('subject', css_class='col-md-6'),
                Column('grading_system', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Subject Grading', css_class='btn-primary')
        )


class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Student
        exclude = ('user', 'student_id')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User Information',
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('phone', css_class='col-md-6'),
                ),
                Row(
                    Column('first_name', css_class='col-md-6'),
                    Column('last_name', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Student Information',
                Row(
                    Column('admission_date', css_class='col-md-6'),
                    Column('current_class', css_class='col-md-6'),
                ),
                Row(
                    Column('date_of_birth', css_class='col-md-6'),
                    Column('gender', css_class='col-md-6'),
                ),
                Row(
                    Column('address', css_class='col-md-6'),
                    Column('city', css_class='col-md-6'),
                ),
                Row(
                    Column('state', css_class='col-md-6'),
                    Column('country', css_class='col-md-6'),
                ),
                Row(
                    Column('blood_group', css_class='col-md-6'),
                    Column('religion', css_class='col-md-6'),
                ),
                Row(
                    Column('is_active', css_class='col-md-6'),
                ),
            ),
            Submit('submit', 'Save Student', css_class='btn-primary')
        )

    def save(self, commit=True):
        student = super().save(commit=False)

        if not student.user_id:
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                user_type='STUDENT',
                phone=self.cleaned_data.get('phone', ''),
            )
            student.user = user
        else:
            user = student.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.phone = self.cleaned_data.get('phone', '')
            user.save()

        if commit:
            student.save()

        return student


class TeacherForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Teacher
        exclude = ('user', 'teacher_id')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User Information',
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('phone', css_class='col-md-6'),
                ),
                Row(
                    Column('first_name', css_class='col-md-6'),
                    Column('last_name', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Teacher Information',
                Row(
                    Column('date_of_birth', css_class='col-md-6'),
                    Column('gender', css_class='col-md-6'),
                ),
                Row(
                    Column('qualification', css_class='col-md-6'),
                    Column('specialization', css_class='col-md-6'),
                ),
                Row(
                    Column('joining_date', css_class='col-md-6'),
                    Column('is_active', css_class='col-md-6'),
                ),
                'subjects',
            ),
            Submit('submit', 'Save Teacher', css_class='btn-primary')
        )

    def save(self, commit=True):
        teacher = super().save(commit=False)

        if not teacher.user_id:
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                user_type='TEACHER',
                phone=self.cleaned_data.get('phone', ''),
            )
            teacher.user = user
        else:
            user = teacher.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.phone = self.cleaned_data.get('phone', '')
            user.save()

        if commit:
            teacher.save()
            self.save_m2m()

        return teacher


class StaffForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Staff
        exclude = ('user', 'staff_id')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User Information',
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('phone', css_class='col-md-6'),
                ),
                Row(
                    Column('first_name', css_class='col-md-6'),
                    Column('last_name', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Staff Information',
                Row(
                    Column('date_of_birth', css_class='col-md-6'),
                    Column('gender', css_class='col-md-6'),
                ),
                Row(
                    Column('department', css_class='col-md-6'),
                    Column('position', css_class='col-md-6'),
                ),
                Row(
                    Column('joining_date', css_class='col-md-6'),
                    Column('is_active', css_class='col-md-6'),
                ),
            ),
            Submit('submit', 'Save Staff', css_class='btn-primary')
        )

    def save(self, commit=True):
        staff = super().save(commit=False)

        if not staff.user_id:
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                user_type='STAFF',
                phone=self.cleaned_data.get('phone', ''),
            )
            staff.user = user
        else:
            user = staff.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.phone = self.cleaned_data.get('phone', '')
            user.save()

        if commit:
            staff.save()

        return staff


class ParentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Parent
        exclude = ('user',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User Information',
                Row(
                    Column('email', css_class='col-md-6'),
                    Column('phone', css_class='col-md-6'),
                ),
                Row(
                    Column('first_name', css_class='col-md-6'),
                    Column('last_name', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Parent Information',
                Row(
                    Column('occupation', css_class='col-md-6'),
                ),
                Row(
                    Column('address', css_class='col-md-6'),
                    Column('city', css_class='col-md-6'),
                ),
                Row(
                    Column('state', css_class='col-md-6'),
                    Column('country', css_class='col-md-6'),
                ),
                'students',
            ),
            Submit('submit', 'Save Parent', css_class='btn-primary')
        )

    def save(self, commit=True):
        parent = super().save(commit=False)

        if not parent.user_id:
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                user_type='PARENT',
                phone=self.cleaned_data.get('phone', ''),
            )
            parent.user = user
        else:
            user = parent.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.phone = self.cleaned_data.get('phone', '')
            user.save()

        if commit:
            parent.save()
            self.save_m2m()

        return parent


class ClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('class_info', css_class='col-md-6'),
                Column('subject', css_class='col-md-6'),
            ),
            Row(
                Column('teacher', css_class='col-md-6'),
                Column('academic_year', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Class Subject', css_class='btn-primary')
        )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('remark', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Attendance', css_class='btn-primary')
        )


class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('weight', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Exam Type', css_class='btn-primary')
        )


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
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

        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date must be after start date")

        if academic_year and start_date and end_date:
            if start_date < academic_year.start_date or end_date > academic_year.end_date:
                raise ValidationError("Exam dates must be within academic year dates")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('exam_type', css_class='col-md-6'),
            ),
            Row(
                Column('academic_year', css_class='col-md-6'),
                Column('semester', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Row(
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Exam', css_class='btn-primary')
        )


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('exam', css_class='col-md-6'),
                Column('student', css_class='col-md-6'),
            ),
            Row(
                Column('subject', css_class='col-md-6'),
                Column('paper', css_class='col-md-6'),
            ),
            Row(
                Column('marks', css_class='col-md-6'),
                Column('grade', css_class='col-md-6'),
            ),
            'remark',
            Submit('submit', 'Save Exam Result', css_class='btn-primary')
        )


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('code', css_class='col-md-6'),
            ),
            Row(
                Column('amount', css_class='col-md-6'),
                Column('is_recurring', css_class='col-md-6'),
            ),
            Row(
                Column('frequency', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Fee Type', css_class='btn-primary')
        )


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('fee_type', css_class='col-md-6'),
                Column('class_level', css_class='col-md-6'),
            ),
            Row(
                Column('academic_year', css_class='col-md-6'),
                Column('amount', css_class='col-md-6'),
            ),
            Row(
                Column('due_date', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Fee Structure', css_class='btn-primary')
        )


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = '__all__'
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student', css_class='col-md-6'),
                Column('fee_structure', css_class='col-md-6'),
            ),
            Row(
                Column('amount_paid', css_class='col-md-6'),
                Column('payment_date', css_class='col-md-6'),
            ),
            Row(
                Column('payment_method', css_class='col-md-6'),
                Column('transaction_id', css_class='col-md-6'),
            ),
            'remarks',
            Submit('submit', 'Save Fee Payment', css_class='btn-primary')
        )


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_class = cleaned_data.get('from_class')
        to_class = cleaned_data.get('to_class')

        if from_class and to_class and from_class == to_class:
            raise ValidationError("From class and To class cannot be the same")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student', css_class='col-md-6'),
                Column('academic_year', css_class='col-md-6'),
            ),
            Row(
                Column('from_class', css_class='col-md-6'),
                Column('to_class', css_class='col-md-6'),
            ),
            Row(
                Column('date', css_class='col-md-6'),
            ),
            'remarks',
            Submit('submit', 'Save Promotion', css_class='btn-primary')
        )


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('class_info', css_class='col-md-6'),
                Column('subject', css_class='col-md-6'),
            ),
            Row(
                Column('teacher', css_class='col-md-6'),
                Column('academic_year', css_class='col-md-6'),
            ),
            Row(
                Column('day', css_class='col-md-6'),
                Column('room', css_class='col-md-6'),
            ),
            Row(
                Column('start_time', css_class='col-md-6'),
                Column('end_time', css_class='col-md-6'),
            ),
            Row(
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Timetable', css_class='btn-primary')
        )


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date must be after start date")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'content',
            Row(
                Column('audience', css_class='col-md-6'),
                Column('is_active', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Notice', css_class='btn-primary')
        )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date must be after start date")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Row(
                Column('location', css_class='col-md-6'),
                Column('audience', css_class='col-md-6'),
            ),
            Row(
                Column('is_active', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Event', css_class='btn-primary')
        )


class LibraryBookForm(forms.ModelForm):
    class Meta:
        model = LibraryBook
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-6'),
                Column('author', css_class='col-md-6'),
            ),
            Row(
                Column('isbn', css_class='col-md-6'),
                Column('publisher', css_class='col-md-6'),
            ),
            Row(
                Column('edition', css_class='col-md-6'),
                Column('category', css_class='col-md-6'),
            ),
            Row(
                Column('quantity', css_class='col-md-6'),
                Column('cover_image', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Book', css_class='btn-primary')
        )


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = '__all__'
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('book', css_class='col-md-6'),
                Column('issued_to', css_class='col-md-6'),
            ),
            Row(
                Column('issue_date', css_class='col-md-6'),
                Column('due_date', css_class='col-md-6'),
            ),
            Row(
                Column('return_date', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            Row(
                Column('fine_amount', css_class='col-md-6'),
            ),
            'remarks',
            Submit('submit', 'Save Book Issue', css_class='btn-primary')
        )