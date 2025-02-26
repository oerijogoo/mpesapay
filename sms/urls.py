from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),

    # Teacher URLs
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),

    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),

    # Enrollment URLs
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/add/', views.add_enrollment, name='add_enrollment'),

    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),

    # Fee Management URLs
    path('fees/pay/', views.pay_fees, name='pay_fees'),
    path('fees/success/', views.fee_payment_success, name='fee_payment_success'),
    path('fees/account/<int:student_id>/', views.student_fee_account, name='student_fee_account'),

    # Marks and Grading URLs
    path('marks/', views.mark_list, name='mark_list'),
    path('marks/add/', views.add_mark, name='add_mark'),

    # Report Card URLs
    path('report-cards/', views.report_card_list, name='report_card_list'),
    path('report-cards/add/', views.add_report_card, name='add_report_card'),

    # Co-curricular Activities URLs
    path('activities/', views.co_curricular_activity_list, name='co_curricular_activity_list'),
    path('activities/add/', views.add_co_curricular_activity, name='add_co_curricular_activity'),
    path('student-activities/', views.student_activity_list, name='student_activity_list'),
    path('student-activities/add/', views.add_student_activity, name='add_student_activity'),
]