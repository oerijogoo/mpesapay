from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class SchoolConfigForm(forms.ModelForm):
    class Meta:
        model = SchoolConfig
        fields = '__all__'
        widgets = {
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

class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = '__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ('user',)
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user', 'admission_number')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ('user',)
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'transaction_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }