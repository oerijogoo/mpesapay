from django import forms
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
            'student': forms.HiddenInput(),
            'paper': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

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
        ('csv', 'CS Upload'),
        ('manual', 'Manual Entry'),
    ]

    entry_type = forms.ChoiceField(choices=ENTRY_TYPE_CHOICES, widget=forms.RadioSelect)
    paper = forms.ModelChoiceField(queryset=Paper.objects.none())
    csv_file = forms.FileField(required=False)
    marks_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10}),
        required=False,
        help_text="Format: Admission Number, Marks (one per line)"
    )

    def __init__(self, *args, **kwargs):
        papers = kwargs.pop('papers', None)
        super().__init__(*args, **kwargs)
        if papers:
            self.fields['paper'].queryset = papers


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