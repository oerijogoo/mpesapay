from django import forms
from django.urls import reverse_lazy

from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'admission_number']
        widgets = {
            'academic_year': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': '/sms/load-semesters/',
                'hx-target': '#id_semester',
                'hx-trigger': 'change'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_semester'
            }),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Always start with empty semester queryset
        self.fields['semester'].queryset = Semester.objects.none()

        # Handle initial data for existing instances
        if self.instance.pk and self.instance.academic_year:
            self.fields['semester'].queryset = self.instance.academic_year.semester_set.order_by('name')

        # Handle form submissions/validation
        if 'academic_year' in self.data:
            try:
                academic_year_id = int(self.data.get('academic_year'))
                self.fields['semester'].queryset = Semester.objects.filter(
                    academic_year_id=academic_year_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass  # Maintain empty queryset

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': '/sms/load-papers/',
                'hx-trigger': 'change',
                'hx-target': '#id_paper'
            }),
            'paper': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paper'].queryset = Paper.objects.none()

        if 'student' in self.data:
            try:
                student_id = int(self.data.get('student'))
                student = Student.objects.get(pk=student_id)
                self.fields['paper'].queryset = Paper.objects.filter(
                    subject__in=student.course.subjects.all()
                )
            except (ValueError, TypeError, Student.DoesNotExist):
                pass

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
        widgets = {
            'min_mark': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_mark': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BulkMarkForm(forms.Form):
    ENTRY_TYPE_CHOICES = [
        ('single', 'Single Entry'),
        ('bulk', 'Bulk CSV Upload'),
    ]

    entry_type = forms.ChoiceField(
        choices=ENTRY_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check-input'}),
        initial='single'
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'hx-get': reverse_lazy('sms:load_papers'),
            'hx-target': '#id_paper',
            'hx-trigger': 'change'
        })
    )

    paper = forms.ModelChoiceField(
        queryset=Paper.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_paper',
            'hx-get': reverse_lazy('sms:load_students'),
            'hx-trigger': 'change',
            'hx-target': '#student-list',
            'disabled': True
        })
    )
    csv_file = forms.FileField(required=False)


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'
        widgets = {
            'academic_year': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': '/load-academic-years/',
                'hx-trigger': 'change'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }



class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = '__all__'
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': '/sms/load-subjects/',
                'hx-trigger': 'change'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'max_mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }