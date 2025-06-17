from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', views.password_change, name='password_change'),

    # School Configura
    path('school-config/', views.school_config_view, name='school_config'),

    # Academic Structure
    path('academic-years/', views.academic_year_list, name='academic_years'),
    path('academic-years/add/', views.academic_year_add, name='academic_year_add'),
    path('academic-years/<int:pk>/edit/', views.academic_year_edit, name='academic_year_edit'),
    path('terms/', views.term_list, name='terms'),
    path('terms/add/', views.term_add, name='term_add'),
    path('terms/<int:pk>/edit/', views.term_edit, name='term_edit'),

    # Class Managemen
    path('classes/', views.class_list, name='classes'),
    path('classes/add/', views.class_add, name='class_add'),
    path('classes/<int:pk>/edit/', views.class_edit, name='class_edit'),

    # Subject Management
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),

    # Staff Management
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.staff_add, name='staff_add'),
    path('staff/<int:pk>/', views.staff_detail, name='staff_detail'),
    path('staff/<int:pk>/edit/', views.staff_edit, name='staff_edit'),

    # Student Management
    path('students/', views.student_list, name='students'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),

    # Parent Management
    path('parents/', views.parent_list, name='parents'),
    path('parents/add/', views.parent_add, name='parent_add'),
    path('parents/<int:pk>/', views.parent_detail, name='parent_detail'),
    path('parents/<int:pk>/edit/', views.parent_edit, name='parent_edit'),

    # Examination System
    path('exams/', views.exam_list, name='exams'),
    path('exams/add/', views.exam_add, name='exam_add'),
    path('exams/<int:pk>/marks/', views.exam_marks, name='exam_marks'),

    # Finance
    path('fees/', views.fee_structure_list, name='fee_structures'),
    path('fees/add/', views.fee_structure_add, name='fee_structure_add'),
    path('payments/', views.payment_list, name='payments'),
    path('payments/add/', views.payment_add, name='payment_add'),

    # Reports
    path('reports/students/', views.student_reports, name='student_reports'),
    path('reports/classes/', views.class_reports, name='class_reports'),
    path('reports/exams/', views.exam_reports, name='exam_reports'),
]