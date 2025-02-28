from django import forms
from .models import Course, Student, Subject, Mark

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'subjects': forms.CheckboxSelectMultiple()
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'admission_number', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.prefetch_related('subjects')

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['subject', 'score']

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if self.student:
            self.fields['subject'].queryset = self.student.enrolled_subjects.all()
        self.fields['student'] = forms.ModelChoiceField(
            queryset=Student.objects.all(),
            widget=forms.HiddenInput(),
            required=False
        )

    def clean_student(self):
        return self.student