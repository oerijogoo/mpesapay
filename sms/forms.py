from django import forms
from .models import (
    Student, Teacher, Course, Enrollment, Attendance, FeePayment,
    Mark, ReportCard, CoCurricularActivity, StudentActivity
)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = '__all__'

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'

class ReportCardForm(forms.ModelForm):
    class Meta:
        model = ReportCard
        fields = '__all__'

class CoCurricularActivityForm(forms.ModelForm):
    class Meta:
        model = CoCurricularActivity
        fields = '__all__'

class StudentActivityForm(forms.ModelForm):
    class Meta:
        model = StudentActivity
        fields = '__all__'