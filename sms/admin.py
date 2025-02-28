from django.contrib import admin
from .models import Grading, Mark, Student, Subject


class GradingAdmin(admin.ModelAdmin):
    list_display = ('grade', 'min_score', 'max_score', 'description')
    ordering = ('-min_score',)  # Order from highest to lowest grade
    search_fields = ('grade', 'description')

    def get_ordering(self, request):
        return ['-min_score']  # Ensure proper ordering in admin


class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'get_grade', 'date_recorded', 'is_absent')
    list_filter = ('subject', 'date_recorded', 'is_absent', 'student__course')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')
    readonly_fields = ('get_grade',)
    list_select_related = ('student', 'subject')

    def get_grade(self, obj):
        return obj.grade

    get_grade.short_description = 'Grade'
    get_grade.admin_order_field = 'score'  # Allows sorting by score to approximate grade order

    fieldsets = (
        (None, {
            'fields': ('student', 'subject', 'score', 'is_absent')
        }),
        ('Grade Information', {
            'fields': ('get_grade',),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = Student.objects.select_related('course')
        if db_field.name == "subject":
            kwargs["queryset"] = Subject.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # Automatically calculate grade on save
        if not obj.is_absent and obj.score is not None:
            try:
                obj.grade = Grading.objects.filter(
                    min_score__lte=obj.score,
                    max_score__gte=obj.score
                ).first().grade
            except AttributeError:
                obj.grade = 'Ungraded'
        super().save_model(request, obj, form, change)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'admission_number', 'course', 'year_of_study', 'semester')
    list_filter = ('course', 'year_of_study', 'semester')
    search_fields = ('first_name', 'last_name', 'admission_number')
    readonly_fields = ('average_score', 'overall_grade')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credit_hours')
    search_fields = ('name', 'code')
    list_filter = ('credit_hours',)


# Custom filter for grades
class GradeListFilter(admin.SimpleListFilter):
    title = 'Grade'
    parameter_name = 'grade'

    def lookups(self, request, model_admin):
        return Grading.objects.values_list('grade', 'grade').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(score__range=(
                Grading.objects.get(grade=self.value()).min_score,
                Grading.objects.get(grade=self.value()).max_score
            ))
        return queryset


# Register models
admin.site.register(Grading, GradingAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)