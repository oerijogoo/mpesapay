from django.urls import path
from . import views

app_name = 'sms'

urlpatterns = [

# Add these new authentication URLs
    path('auth/student/signup/', views.student_signup, name='student_signup'),
    path('auth/teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('student/profile/', views.student_profile, name='student_profile'),
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('student/new/', views.student_create, name='student_create'),
    path('student/<int:pk>/edit/', views.student_update, name='student_update'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('student/<int:pk>/report/', views.student_report, name='student_report'),
    path('student/<int:pk>/pdf/', views.generate_pdf_report, name='generate_pdf'),
    path('load-students/', views.load_students, name='load_students'),
    path('reports/students/', views.student_report_list, name='report_student_list'),

    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('course/new/', views.course_create, name='course_create'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/edit/', views.course_update, name='course_update'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Subject URLs
    path('subjects/', views.subject_list, name='subject_list'),
    path('subject/new/', views.subject_create, name='subject_create'),
    path('subject/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:pk>/edit/', views.subject_update, name='subject_update'),
    path('subject/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # Academic Year URLs
    path('year/', views.academic_year_list, name='academic_year_list'),  # No pk
    path('year/new/', views.academic_year_create, name='academic_year_create'),
    path('year/<int:pk>/', views.academic_year_detail, name='academic_year_detail'),
    path('year/<int:pk>/edit/', views.academic_year_update, name='academic_year_update'),
    path('year/<int:pk>/delete/', views.academic_year_delete, name='academic_year_delete'),

    path('load-academic-years/', views.load_academic_years, name='load_academic_years'),

    # Semester URLs
    path('load-semesters/', views.load_semesters, name='load_semesters'),
    path('semesters/', views.semester_list, name='semester_list'),
    path('semester/new/', views.semester_create, name='semester_create'),
    path('semester/<int:pk>/', views.semester_detail, name='semester_detail'),
    path('semester/<int:pk>/edit/', views.semester_update, name='semester_update'),
    path('semester/<int:pk>/delete/', views.semester_delete, name='semester_delete'),

    path('reports/semesters/', views.semester_report_list, name='semester_report_list'),
    path('reports/semesters/<int:semester_id>/', views.semester_report, name='semester_report'),

    # Grade URLs
    path('grades/', views.grade_list, name='grade_list'),
    path('grade/new/', views.grade_create, name='grade_create'),
    path('grade/<int:pk>/edit/', views.grade_update, name='grade_update'),
    path('grade/<int:pk>/delete/', views.grade_delete, name='grade_delete'),

    # Add these patterns
    path('papers/', views.paper_list, name='paper_list'),
    path('paper/new/', views.paper_create, name='paper_create'),
    path('paper/<int:pk>/edit/', views.paper_update, name='paper_update'),
    path('paper/<int:pk>/delete/', views.paper_delete, name='paper_delete'),
    path('load-papers/', views.load_papers, name='load_papers'),

# Report URLs
#     path('reports/courses/', views.course_report_list, name='course_report_list'),
#     path('reports/courses/<int:course_id>/', views.course_report, name='course_report'),
#     path('reports/semesters/', views.semester_report_list, name='semester_report_list'),
#     path('reports/semesters/<int:semester_id>/', views.semester_report, name='semester_report'),

    path('reports/courses/', views.course_report_list, name='course_report_list'),
    path('reports/courses/<int:course_id>/', views.course_report, name='course_report'),
    path('reports/semesters/', views.semester_report_list, name='semester_report_list'),


    # Mark URLs
    path('marks/bulk-entry/', views.bulk_mark_entry, name='bulk_mark_entry'),

    path('student/<int:pk>/progress/',
         views.student_progressive_report,
         name='student_progressive_report'),
    path('student/<int:pk>/progress/pdf/',
         views.student_progressive_report_pdf,
         name='student_progressive_report_pdf'),



    # path('marks/add/', views.mark_create, name='mark_create'),
    # path('mark/<int:pk>/edit/', views.mark_update, name='mark_update'),
    # path('mark/<int:pk>/delete/', views.mark_delete, name='mark_delete'),
    path('dashboard/', views.smart_dashboard, name='dashboard'),


]