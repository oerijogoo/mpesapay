from django.urls import path
from . import views
from .views import (
    CourseListView, CourseCreateView, CourseUpdateView,
    StudentListView, StudentCreateView, StudentUpdateView,
    MarkListView, MarkCreateView, SubjectListView,
    SubjectCreateView, StudentDetailView, AttendanceListView, AttendanceCreateView, FeeStructureListView,
    FeeStructureCreateView, PaymentListView, PaymentCreateView
)

urlpatterns = [
    # Subjects
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', SubjectCreateView.as_view(), name='subject_create'),

    # Courses
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/add/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),

    # Students
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/add/', StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/marks/add/', MarkCreateView.as_view(), name='mark_create'),

    # Marks
    path('marks/', MarkListView.as_view(), name='mark_list'),

    # Reports & Exports
    path('reports/academic/', views.student_academic_report, name='academic_report'),
    path('students/<int:pk>/report/', views.generate_student_report_pdf, name='student_report_pdf'),
    path('export/<str:format_type>/<str:model_name>/', views.export_data, name='export_data'),  # Added this line

# Attendance
path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
path('attendance/add/', AttendanceCreateView.as_view(), name='attendance_create'),

# Financial
path('fees/', FeeStructureListView.as_view(), name='fee_structure_list'),
path('fees/add/', FeeStructureCreateView.as_view(), name='fee_structure_create'),
path('payments/', PaymentListView.as_view(), name='payment_list'),
path('payments/add/', PaymentCreateView.as_view(), name='payment_create'),
]