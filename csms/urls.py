# urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views

app_name = 'csms'

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name='auth/password_change.html'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),

    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # School Configuration
    path('school-settings/', views.SchoolSettingsView.as_view(), name='school_settings'),

    # Academic Structure
    path('academic-years/', views.AcademicYearListView.as_view(), name='academic_year_list'),
    path('academic-years/create/', views.AcademicYearCreateView.as_view(), name='academic_year_create'),
    path('academic-years/<int:pk>/update/', views.AcademicYearUpdateView.as_view(), name='academic_year_update'),
    path('academic-years/<int:pk>/delete/', views.AcademicYearDeleteView.as_view(), name='academic_year_delete'),

    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semesters/create/', views.SemesterCreateView.as_view(), name='semester_create'),
    path('semesters/<int:pk>/update/', views.SemesterUpdateView.as_view(), name='semester_update'),
    path('semesters/<int:pk>/delete/', views.SemesterDeleteView.as_view(), name='semester_delete'),

    path('academic-levels/', views.AcademicLevelListView.as_view(), name='academic_level_list'),
    path('academic-levels/create/', views.AcademicLevelCreateView.as_view(), name='academic_level_create'),
    path('academic-levels/<int:pk>/update/', views.AcademicLevelUpdateView.as_view(), name='academic_level_update'),
    path('academic-levels/<int:pk>/delete/', views.AcademicLevelDeleteView.as_view(), name='academic_level_delete'),

    # Course and Subject Management
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/<int:pk>/update/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),

    path('course-subjects/', views.CourseSubjectListView.as_view(), name='course_subject_list'),
    path('course-subjects/create/', views.CourseSubjectCreateView.as_view(), name='course_subject_create'),
    path('course-subjects/<int:pk>/update/', views.CourseSubjectUpdateView.as_view(), name='course_subject_update'),
    path('course-subjects/<int:pk>/delete/', views.CourseSubjectDeleteView.as_view(), name='course_subject_delete'),

    # Grading System
    path('grading-scales/', views.GradingScaleListView.as_view(), name='grading_scale_list'),
    path('grading-scales/create/', views.GradingScaleCreateView.as_view(), name='grading_scale_create'),
    path('grading-scales/<int:pk>/', views.GradingScaleDetailView.as_view(), name='grading_scale_detail'),
    path('grading-scales/<int:pk>/update/', views.GradingScaleUpdateView.as_view(), name='grading_scale_update'),
    path('grading-scales/<int:pk>/delete/', views.GradingScaleDeleteView.as_view(), name='grading_scale_delete'),

    path('grading-scales/<int:grading_scale_id>/grades/create/', views.GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/update/', views.GradeUpdateView.as_view(), name='grade_update'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),

    path('subject-gradings/', views.SubjectGradingListView.as_view(), name='subject_grading_list'),
    path('subject-gradings/create/', views.SubjectGradingCreateView.as_view(), name='subject_grading_create'),
    path('subject-gradings/<int:pk>/update/', views.SubjectGradingUpdateView.as_view(), name='subject_grading_update'),
    path('subject-gradings/<int:pk>/delete/', views.SubjectGradingDeleteView.as_view(), name='subject_grading_delete'),

    # People Management
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/create/', views.TeacherCreateView.as_view(), name='teacher_create'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),

    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/create/', views.StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/report/', views.StudentReportView.as_view(), name='student_report'),
    path('students/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/update/', views.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    # Class Management
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('classes/create/', views.ClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('classes/<int:pk>/update/', views.ClassUpdateView.as_view(), name='class_update'),
    path('classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),

    path('class-subjects/', views.ClassSubjectListView.as_view(), name='class_subject_list'),
    path('class-subjects/create/', views.ClassSubjectCreateView.as_view(), name='class_subject_create'),
    path('class-subjects/<int:pk>/update/', views.ClassSubjectUpdateView.as_view(), name='class_subject_update'),
    path('class-subjects/<int:pk>/delete/', views.ClassSubjectDeleteView.as_view(), name='class_subject_delete'),

    # Exam System
    path('exam-types/', views.ExamTypeListView.as_view(), name='exam_type_list'),
    path('exam-types/create/', views.ExamTypeCreateView.as_view(), name='exam_type_create'),
    path('exam-types/<int:pk>/update/', views.ExamTypeUpdateView.as_view(), name='exam_type_update'),
    path('exam-types/<int:pk>/delete/', views.ExamTypeDeleteView.as_view(), name='exam_type_delete'),

    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/create/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('exams/<int:pk>/update/', views.ExamUpdateView.as_view(), name='exam_update'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),

    path('exam-schedules/', views.ExamScheduleListView.as_view(), name='exam_schedule_list'),
    path('exam-schedules/create/', views.ExamScheduleCreateView.as_view(), name='exam_schedule_create'),
    path('exam-schedules/<int:pk>/update/', views.ExamScheduleUpdateView.as_view(), name='exam_schedule_update'),
    path('exam-schedules/<int:pk>/delete/', views.ExamScheduleDeleteView.as_view(), name='exam_schedule_delete'),

    path('marks/', views.MarkListView.as_view(), name='mark_list'),
    path('marks/create/', views.MarkCreateView.as_view(), name='mark_create'),
    path('marks/<int:pk>/update/', views.MarkUpdateView.as_view(), name='mark_update'),
    path('marks/<int:pk>/delete/', views.MarkDeleteView.as_view(), name='mark_delete'),
    path('marks/<int:mark_id>/grade/', views.GradeAllocationCreateView.as_view(), name='grade_allocation_create'),
    path('grade-allocations/<int:pk>/update/', views.GradeAllocationUpdateView.as_view(), name='grade_allocation_update'),
    path('grade-allocations/<int:pk>/delete/', views.GradeAllocationDeleteView.as_view(), name='grade_allocation_delete'),

    path('academic-reports/', views.AcademicReportListView.as_view(), name='academic_report_list'),
    path('academic-reports/create/', views.AcademicReportCreateView.as_view(), name='academic_report_create'),
    path('academic-reports/<int:pk>/', views.AcademicReportDetailView.as_view(), name='academic_report_detail'),
    path('academic-reports/<int:pk>/update/', views.AcademicReportUpdateView.as_view(), name='academic_report_update'),
    path('academic-reports/<int:pk>/delete/', views.AcademicReportDeleteView.as_view(), name='academic_report_delete'),

    # Financial Management
    path('fee-types/', views.FeeTypeListView.as_view(), name='fee_type_list'),
    path('fee-types/create/', views.FeeTypeCreateView.as_view(), name='fee_type_create'),
    path('fee-types/<int:pk>/update/', views.FeeTypeUpdateView.as_view(), name='fee_type_update'),
    path('fee-types/<int:pk>/delete/', views.FeeTypeDeleteView.as_view(), name='fee_type_delete'),

    path('fee-structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('fee-structures/create/', views.FeeStructureCreateView.as_view(), name='fee_structure_create'),
    path('fee-structures/<int:pk>/update/', views.FeeStructureUpdateView.as_view(), name='fee_structure_update'),
    path('fee-structures/<int:pk>/delete/', views.FeeStructureDeleteView.as_view(), name='fee_structure_delete'),

    path('student-fees/', views.StudentFeeListView.as_view(), name='student_fee_list'),
    path('student-fees/create/', views.StudentFeeCreateView.as_view(), name='student_fee_create'),
    path('student-fees/<int:pk>/update/', views.StudentFeeUpdateView.as_view(), name='student_fee_update'),
    path('student-fees/<int:pk>/delete/', views.StudentFeeDeleteView.as_view(), name='student_fee_delete'),

    # Calendar and Attendance
    path('academic-calendar/', views.AcademicCalendarListView.as_view(), name='academic_calendar_list'),
    path('academic-calendar/create/', views.AcademicCalendarCreateView.as_view(), name='academic_calendar_create'),
    path('academic-calendar/<int:pk>/update/', views.AcademicCalendarUpdateView.as_view(), name='academic_calendar_update'),
    path('academic-calendar/<int:pk>/delete/', views.AcademicCalendarDeleteView.as_view(), name='academic_calendar_delete'),

    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/<int:pk>/update/', views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),

    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/create/', views.NotificationCreateView.as_view(), name='notification_create'),
    path('notifications/<int:pk>/update/', views.NotificationUpdateView.as_view(), name='notification_update'),
    path('notifications/<int:pk>/delete/', views.NotificationDeleteView.as_view(), name='notification_delete'),

    # Bulk Operations
    path('bulk/marks/', views.BulkMarkEntryView.as_view(), name='bulk_mark_entry'),
    path('bulk/students/', views.BulkStudentCreationView.as_view(), name='bulk_student_creation'),

    # AJAX Views
    path('ajax/get-papers/', views.get_papers_for_subject, name='ajax_get_papers'),
    path('ajax/get-students/', views.get_students_for_class, name='ajax_get_students'),
]