from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.utils.html import format_html
from .models import *

# ==================== User Management ====================
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# ==================== School Configuration ====================
@admin.register(SchoolConfig)
class SchoolConfigAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'location', 'phone', 'email')
    fieldsets = (
        ('Basic Information', {'fields': ('school_name', 'motto', 'school_logo')}),
        ('Contact Information', {'fields': ('location', 'address', 'phone', 'email', 'website')}),
        ('System Configuration', {'fields': ('student_prefix', 'current_academic_year', 'current_term')}),
    )

# ==================== Academic Structure ====================
class TermInline(admin.TabularInline):
    model = Term
    extra = 0
    fields = ('term', 'start_date', 'end_date', 'is_active')
    readonly_fields = ('is_active',)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_editable = ('is_active',)
    inlines = [TermInline]
    actions = ['set_as_current']

    def set_as_current(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one academic year.", level='error')
            return
        year = queryset.first()
        SchoolConfig.objects.all().update(current_academic_year=year)
        Term.objects.filter(academic_year=year).update(is_active=False)
        self.message_user(request, f"{year.name} set as current academic year")

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('academic_year', 'get_term_display', 'start_date', 'end_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('academic_year', 'term')
    actions = ['set_as_current']

    def set_as_current(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one term.", level='error')
            return
        term = queryset.first()
        SchoolConfig.objects.all().update(current_term=term)
        Term.objects.filter(academic_year=term.academic_year).update(is_active=False)
        term.is_active = True
        term.save()
        self.message_user(request, f"{term.get_term_display()} of {term.academic_year.name} set as current term")

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'next_class')
    list_select_related = ('next_class',)
    search_fields = ('name', 'code')

# ==================== Subjects Management ====================
class SubSubjectInline(admin.TabularInline):
    model = SubSubject
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_core')
    list_editable = ('is_core',)
    search_fields = ('name', 'code')
    inlines = [SubSubjectInline]

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_level', 'subject', 'is_compulsory')
    list_filter = ('class_level', 'is_compulsory')
    list_editable = ('is_compulsory',)
    search_fields = ('subject__name', 'class_level__name')

# ==================== Grading System ====================
@admin.register(GradingSystem)
class GradingSystemAdmin(admin.ModelAdmin):
    list_display = ('subject', 'grade_name', 'min_score', 'max_score', 'points', 'remark')
    list_filter = ('subject',)
    ordering = ('subject', 'min_score')

# ==================== Staff Management ====================
class TeacherInline(admin.StackedInline):
    model = Teacher
    extra = 0
    filter_horizontal = ('subjects',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'type', 'phone', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'staff_id')
    inlines = [TeacherInline]
    fieldsets = (
        (None, {'fields': ('user', 'staff_id', 'type', 'is_active')}),
        ('Personal Info', {'fields': ('phone', 'address', 'photo')}),
    )

# ==================== Student & Parent Management ====================
class StudentInline(admin.TabularInline):
    model = Student.parents.through
    extra = 1
    verbose_name = "Child"
    verbose_name_plural = "Children"


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'occupation')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Personal Info', {'fields': ('phone', 'address', 'occupation', 'photo')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add a custom field for students in the form
        form.base_fields['_students'] = forms.ModelMultipleChoiceField(
            queryset=Student.objects.all(),
            required=False,
            label='Children',
            widget=FilteredSelectMultiple('students', False)
        )
        if obj:
            form.base_fields['_students'].initial = obj.student_set.all()
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if '_students' in form.cleaned_data:
            obj.student_set.set(form.cleaned_data['_students'])

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'current_class', 'gender', 'is_active')
    list_filter = ('current_class', 'gender', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'admission_number')
    filter_horizontal = ('parents',)
    fieldsets = (
        (None, {'fields': ('user', 'admission_number', 'current_class', 'is_active')}),
        ('Personal Info', {'fields': ('gender', 'date_of_birth', 'photo')}),
        ('Parents/Guardians', {'fields': ('parents',)}),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            school_config = SchoolConfig.objects.first()
            if school_config:
                last_student = Student.objects.order_by('-id').first()
                last_id = int(last_student.admission_number[len(school_config.student_prefix):]) if last_student else 0
                obj.admission_number = f"{school_config.student_prefix}{last_id + 1:04d}"
        super().save_model(request, obj, form, change)

# ==================== Examination System ====================
class StudentMarkInline(admin.TabularInline):
    model = StudentMark
    extra = 0
    readonly_fields = ('grade', 'points', 'remark')
    fields = ('student', 'subject', 'marks', 'grade', 'points', 'remark')

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    ordering = ('weight',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'term', 'exam_type', 'start_date', 'end_date')
    list_filter = ('term__academic_year', 'term', 'exam_type')
    inlines = [StudentMarkInline]

@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks', 'grade', 'points')
    list_filter = ('exam__term__academic_year', 'exam__term', 'exam', 'subject')
    search_fields = ('student__user__first_name', 'student__user__last_name')
    readonly_fields = ('grade', 'points', 'remark', 'date_recorded')

# ==================== Finance Management ====================
@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('class_level', 'term', 'amount')
    list_filter = ('term__academic_year', 'term', 'class_level')
    search_fields = ('class_level__name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'student', 'fee_structure', 'amount_paid', 'payment_method', 'transaction_date')
    list_filter = ('fee_structure__term', 'payment_method')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'receipt_number')
    readonly_fields = ('transaction_date',)
    date_hierarchy = 'transaction_date'