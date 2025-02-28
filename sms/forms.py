from django import forms
from .models import (
    Course, Student, Subject, Mark,
    Attendance, FeeStructure, Payment
)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'credit_hours': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
            'duration_years': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'admission_number',
            'course', 'year_of_study', 'semester', 'date_of_birth'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'year_of_study': forms.Select(choices=Student.YEAR_CHOICES),
            'semester': forms.Select(choices=Student.SEMESTER_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.prefetch_related('subjects')


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'course',
            'year_of_study', 'semester'
        ]
        widgets = {
            'year_of_study': forms.Select(choices=Student.YEAR_CHOICES),
            'semester': forms.Select(choices=Student.SEMESTER_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['subject', 'score', 'is_absent']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'is_absent': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if self.student:
            self.fields['subject'].queryset = self.student.enrolled_subjects.all()

    def clean(self):
        cleaned_data = super().clean()
        is_absent = cleaned_data.get('is_absent')
        score = cleaned_data.get('score')

        if is_absent and score is not None:
            raise forms.ValidationError("Score must be empty when marked absent")
        if not is_absent and score is None:
            raise forms.ValidationError("Score is required when not absent")

        return cleaned_data


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'subject', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=Attendance.STATUS_CHOICES)
        }


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'
        widgets = {
            'academic_year': forms.TextInput(attrs={'placeholder': 'YYYY-YYYY'}),
            'tuition_fee': forms.NumberInput(attrs={'min': 0}),
            'registration_fee': forms.NumberInput(attrs={'min': 0}),
            'examination_fee': forms.NumberInput(attrs={'min': 0})
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'payment_method', 'receipt_number']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_method': forms.Select(choices=[
                ('MPesa', 'MPesa'),
                ('Cash', 'Cash'),
                ('Bank', 'Bank Transfer')
            ])
        }