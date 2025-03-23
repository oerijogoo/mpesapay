
from .models import *
from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats



class PaperInline(admin.TabularInline):
    model = Paper
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course_count')
    search_fields = ('name', 'code')
    inlines = [PaperInline]

    def course_count(self, obj):
        return obj.course_set.count()

    course_count.short_description = 'Courses Using'



@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'duration_days')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'

    def duration_days(self, obj):
        return (obj.end_date - obj.start_date).days

    duration_days.short_description = 'Duration (days)'


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'start_date', 'end_date')
    list_filter = ('academic_year',)
    ordering = ('-academic_year__start_date', 'start_date')



@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'paper', 'marks_obtained', 'percentage', 'date')
    list_filter = ('student__course', 'paper__subject')
    search_fields = ('student__admission_number', 'paper__name')
    date_hierarchy = 'date'

    def percentage(self, obj):
        return f"{(obj.marks_obtained / obj.paper.max_mark * 100):.1f}%"

    percentage.short_description = 'Percentage'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'min_mark', 'max_mark', 'description')
    ordering = ('-min_mark',)

    def description(self, obj):
        return f"{obj.grade} ({obj.min_mark}-{obj.max_mark})"

    description.short_description = 'Grade Range'


# Optional: If you need to customize the Paper admin separately
@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'max_mark')
    list_filter = ('subject',)
    search_fields = ('name', 'subject__name')


# ---------- Export Functionality ----------
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('admission_number', 'first_name', 'last_name', 'course__name',
                  'academic_year__name', 'semester__name')
        export_order = fields


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        fields = ('name', 'code', 'subject_count')
        export_order = fields

    def dehydrate_subject_count(self, course):
        return course.subjects.count()


# ---------- Custom Admin Actions ----------
def set_graduated(modeladmin, request, queryset):
    queryset.update(status='graduated')


set_graduated.short_description = "Mark selected students as graduated"


def recalculate_grades(modeladmin, request, queryset):
    for student in queryset:
        # Add your grade recalculation logic here
        student.save()


recalculate_grades.short_description = "Recalculate grades for selected students"


# ---------- Custom Filters ----------
class AcademicYearFilter(admin.SimpleListFilter):
    title = 'Academic Year'
    parameter_name = 'academic_year'

    def lookups(self, request, model_admin):
        return AcademicYear.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(academic_year_id=self.value())
        return queryset

# ---------- Custom Admin Forms ----------
class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date")
        return cleaned_data


# ---------- Bulk Edit Mixin ----------
class BulkEditMixin:
    def get_changelist_form(self, request, **kwargs):
        return forms.modelform_factory(self.model, fields=self.list_editable)


# ---------- Enhanced Admin Classes ----------

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('admission_number', 'student_name', 'course', 'status_badge',
                    'semester', 'grade_average')
    list_editable = ('semester',)  # Changed from current_semester to semester
    list_filter = ('academic_year', 'course', 'status')  # Simplified filter
    search_fields = ('admission_number', 'first_name', 'last_name')

    fieldsets = (
        (None, {
            'fields': ('admission_number', ('first_name', 'last_name'), 'picture')
        }),
        ('Academic Details', {
            'fields': ('course', 'academic_year', 'semester', 'status')
        }),
    )

    def student_name(self, obj):
        return f"{obj.last_name}, {obj.first_name}"

    student_name.admin_order_field = 'last_name'
    student_name.short_description = 'Student Name'

    def status_badge(self, obj):
        color_map = {
            'active': 'green',
            'inactive': 'orange',
            'graduated': 'blue'
        }
        return format_html(
            '<span style="color: {color}; font-weight: bold;">⬤</span> {status}',
            color=color_map.get(obj.status, 'gray'),
            status=obj.get_status_display()
        )

    status_badge.short_description = 'Status'

    def grade_average(self, obj):
        avg = Mark.objects.filter(student=obj).aggregate(Avg('marks_obtained'))['marks_obtained__avg']
        return f"{avg:.2f}%" if avg else "N/A"

    grade_average.short_description = 'Average'


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ('name', 'code', 'student_count', 'subject_list')
    actions = ['update_subject_count']
    filter_horizontal = ('subjects',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            student_count=Count('student')
        )

    def student_count(self, obj):
        return obj.student_count

    student_count.admin_order_field = 'student_count'

    def subject_list(self, obj):
        return ", ".join(s.name for s in obj.subjects.all())

    subject_list.short_description = 'Subjects'

    def update_subject_count(self, request, queryset):
        for course in queryset:
            course.subject_count = course.subjects.count()
            course.save()

    update_subject_count.short_description = "Update subject counts"


# ---------- Admin Site Customization ----------
admin.site.site_header = "School Management System Admin"
admin.site.site_title = "SMS Admin Portal"
admin.site.index_title = "Welcome to School Management System"


class CustomAdminSite(admin.AdminSite):
    site_header = "SMS Administration"
    site_title = "SMS Admin"
    index_title = "Dashboard"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Customize app order
        return sorted(app_list, key=lambda x: x['name'])

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
