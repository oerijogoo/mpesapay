from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # School
    path('school/', views.SchoolView.as_view(), name='school_view'),

    # Academic Year
    path('academic-years/', views.AcademicYearListView.as_view(), name='academic_year_list'),
    path('academic-years/add/', views.AcademicYearCreateView.as_view(), name='academic_year_create'),
    path('academic-years/<int:pk>/edit/', views.AcademicYearUpdateView.as_view(), name='academic_year_update'),
    path('academic-years/<int:pk>/delete/', views.AcademicYearDeleteView.as_view(), name='academic_year_delete'),

    # Semester
    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semesters/add/', views.SemesterCreateView.as_view(), name='semester_create'),
    path('semesters/<int:pk>/edit/', views.SemesterUpdateView.as_view(), name='semester_update'),
    path('semesters/<int:pk>/delete/', views.SemesterDeleteView.as_view(), name='semester_delete'),

    # Department
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Course
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # Subject
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),

    # Paper
    path('subjects/<int:subject_pk>/papers/add/', views.PaperCreateView.as_view(), name='paper_create'),
    path('papers/<int:pk>/edit/', views.PaperUpdateView.as_view(), name='paper_update'),
    path('papers/<int:pk>/delete/', views.PaperDeleteView.as_view(), name='paper_delete'),

    # Grade Scale
    path('grade-scales/', views.GradeScaleListView.as_view(), name='grade_scale_list'),
    path('grade-scales/add/', views.GradeScaleCreateView.as_view(), name='grade_scale_create'),
    path('grade-scales/<int:pk>/edit/', views.GradeScaleUpdateView.as_view(), name='grade_scale_update'),
    path('grade-scales/<int:pk>/delete/', views.GradeScaleDeleteView.as_view(), name='grade_scale_delete'),

    # Grade
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/add/', views.GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/edit/', views.GradeUpdateView.as_view(), name='grade_update'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),

    # Subject Grade Scale
    path('subjects/<int:pk>/grade-scale/', views.SubjectGradeScaleCreateView.as_view(),
         name='subject_grade_scale_create'),
    path('subject-grade-scales/<int:pk>/edit/', views.SubjectGradeScaleUpdateView.as_view(),
         name='subject_grade_scale_update'),
    path('subject-grade-scales/<int:pk>/delete/', views.SubjectGradeScaleDeleteView.as_view(),
         name='subject_grade_scale_delete'),

    # Class Level
    path('class-levels/', views.ClassLevelListView.as_view(), name='class_level_list'),
    path('class-levels/add/', views.ClassLevelCreateView.as_view(), name='class_level_create'),
    path('class-levels/<int:pk>/edit/', views.ClassLevelUpdateView.as_view(), name='class_level_update'),
    path('class-levels/<int:pk>/delete/', views.ClassLevelDeleteView.as_view(), name='class_level_delete'),

    # Class
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('classes/add/', views.ClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/edit/', views.ClassUpdateView.as_view(), name='class_update'),
    path('classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),

    # Student
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # Staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/add/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),

    # Class Subject
    path('class-subjects/', views.ClassSubjectListView.as_view(), name='class_subject_list'),
    path('class-subjects/add/', views.ClassSubjectCreateView.as_view(), name='class_subject_create'),
    path('class-subjects/<int:pk>/edit/', views.ClassSubjectUpdateView.as_view(), name='class_subject_update'),
    path('class-subjects/<int:pk>/delete/', views.ClassSubjectDeleteView.as_view(), name='class_subject_delete'),

    # Enrollment
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/add/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/bulk/', views.BulkEnrollmentView.as_view(), name='bulk_enrollment'),
    path('enrollments/<int:pk>/edit/', views.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    # Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/bulk/', views.BulkAttendanceView.as_view(), name='bulk_attendance'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),

    # Exam Type
    path('exam-types/', views.ExamTypeListView.as_view(), name='exam_type_list'),
    path('exam-types/add/', views.ExamTypeCreateView.as_view(), name='exam_type_create'),
    path('exam-types/<int:pk>/edit/', views.ExamTypeUpdateView.as_view(), name='exam_type_update'),
    path('exam-types/<int:pk>/delete/', views.ExamTypeDeleteView.as_view(), name='exam_type_delete'),

    # Exam
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/add/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/edit/', views.ExamUpdateView.as_view(), name='exam_update'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),

    # Exam Schedule
    path('exam-schedules/', views.ExamScheduleListView.as_view(), name='exam_schedule_list'),
    path('exam-schedules/add/', views.ExamScheduleCreateView.as_view(), name='exam_schedule_create'),
    path('exam-schedules/<int:pk>/edit/', views.ExamScheduleUpdateView.as_view(), name='exam_schedule_update'),
    path('exam-schedules/<int:pk>/delete/', views.ExamScheduleDeleteView.as_view(), name='exam_schedule_delete'),

    # Exam Result
    path('exam-results/', views.ExamResultListView.as_view(), name='exam_result_list'),
    path('exam-results/add/', views.ExamResultCreateView.as_view(), name='exam_result_create'),
    path('exam-results/<int:pk>/edit/', views.ExamResultUpdateView.as_view(), name='exam_result_update'),
    path('exam-results/<int:pk>/delete/', views.ExamResultDeleteView.as_view(), name='exam_result_delete'),

    # Subject Result
    path('subject-results/', views.SubjectResultListView.as_view(), name='subject_result_list'),
    path('subject-results/add/', views.SubjectResultCreateView.as_view(), name='subject_result_create'),
    path('subject-results/<int:pk>/edit/', views.SubjectResultUpdateView.as_view(), name='subject_result_update'),
    path('subject-results/<int:pk>/delete/', views.SubjectResultDeleteView.as_view(), name='subject_result_delete'),

    # Promotion
    path('promotions/', views.PromotionListView.as_view(), name='promotion_list'),
    path('promotions/add/', views.PromotionCreateView.as_view(), name='promotion_create'),
    path('promotions/<int:pk>/edit/', views.PromotionUpdateView.as_view(), name='promotion_update'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion_delete'),

    # Report Comment
    path('report-comments/', views.ReportCommentListView.as_view(), name='report_comment_list'),
    path('report-comments/add/', views.ReportCommentCreateView.as_view(), name='report_comment_create'),
    path('report-comments/<int:pk>/edit/', views.ReportCommentUpdateView.as_view(), name='report_comment_update'),
    path('report-comments/<int:pk>/delete/', views.ReportCommentDeleteView.as_view(), name='report_comment_delete'),

    # Notification
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/add/', views.NotificationCreateView.as_view(), name='notification_create'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('notifications/<int:pk>/edit/', views.NotificationUpdateView.as_view(), name='notification_update'),
    path('notifications/<int:pk>/delete/', views.NotificationDeleteView.as_view(), name='notification_delete'),

    # AJAX URLs
    path('ajax/get-papers-for-subject/', views.get_papers_for_subject, name='get_papers_for_subject'),
    path('ajax/get-students-for-class/', views.get_students_for_class, name='get_students_for_class'),
    path('ajax/get-subjects-for-class/', views.get_subjects_for_class, name='get_subjects_for_class'),
    path('ajax/get-subject-for-class-subject/', views.get_subject_for_class_subject,
         name='get_subject_for_class_subject'),
    path('ajax/get-grade-scale-for-subject/', views.get_grade_scale_for_subject, name='get_grade_scale_for_subject'),
]