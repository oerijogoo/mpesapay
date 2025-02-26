from django.contrib import admin
from .models import (
    AcademicYear, Term, Subject, Student, Teacher, Course, Enrollment,
    StudentFeeAccount, FeePayment, Mark, GradingSystem, ReportCard,
    CoCurricularActivity, StudentActivity
)

admin.site.register(AcademicYear)
admin.site.register(Term)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(StudentFeeAccount)
admin.site.register(FeePayment)
admin.site.register(Mark)
admin.site.register(GradingSystem)
admin.site.register(ReportCard)
admin.site.register(CoCurricularActivity)
admin.site.register(StudentActivity)