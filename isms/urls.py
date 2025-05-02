from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'isms'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='isms/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # School Config
    path('school-config/', views.SchoolConfigUpdateView.as_view(), name='school_config'),

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

    # Subject URLs
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/<int:pk>/update/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),

    # Paper
    path('papers/', views.PaperListView.as_view(), name='paper_list'),
    path('papers/add/', views.PaperCreateView.as_view(), name='paper_create'),
    path('papers/<int:pk>/edit/', views.PaperUpdateView.as_view(), name='paper_update'),
    path('papers/<int:pk>/delete/', views.PaperDeleteView.as_view(), name='paper_delete'),

    # Grading System
    path('grading-systems/', views.GradingSystemListView.as_view(), name='grading_system_list'),
    path('grading-systems/add/', views.GradingSystemCreateView.as_view(), name='grading_system_create'),
    path('grading-systems/<int:pk>/edit/', views.GradingSystemUpdateView.as_view(), name='grading_system_update'),
    path('grading-systems/<int:pk>/delete/', views.GradingSystemDeleteView.as_view(), name='grading_system_delete'),

    # Grade
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/add/', views.GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/edit/', views.GradeUpdateView.as_view(), name='grade_update'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),

    # Subject Grading
    path('subject-gradings/', views.SubjectGradingListView.as_view(), name='subject_grading_list'),
    path('subject-gradings/add/', views.SubjectGradingCreateView.as_view(), name='subject_grading_create'),
    path('subject-gradings/<int:pk>/edit/', views.SubjectGradingUpdateView.as_view(), name='subject_grading_update'),
    path('subject-gradings/<int:pk>/delete/', views.SubjectGradingDeleteView.as_view(), name='subject_grading_delete'),

    # Student
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # Teacher
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/', views.TeacherCreateView.as_view(), name='teacher_create'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),

    # Staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/add/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),

    # Parent
    path('parents/', views.ParentListView.as_view(), name='parent_list'),
    path('parents/add/', views.ParentCreateView.as_view(), name='parent_create'),
    path('parents/<int:pk>/', views.ParentDetailView.as_view(), name='parent_detail'),
    path('parents/<int:pk>/edit/', views.ParentUpdateView.as_view(), name='parent_update'),
    path('parents/<int:pk>/delete/', views.ParentDeleteView.as_view(), name='parent_delete'),

    # Class Subject
    path('class-subjects/', views.ClassSubjectListView.as_view(), name='class_subject_list'),
    path('class-subjects/add/', views.ClassSubjectCreateView.as_view(), name='class_subject_create'),
    path('class-subjects/<int:pk>/edit/', views.ClassSubjectUpdateView.as_view(), name='class_subject_update'),
    path('class-subjects/<int:pk>/delete/', views.ClassSubjectDeleteView.as_view(), name='class_subject_delete'),

    # Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),
    path('attendance/bulk/', views.bulk_attendance, name='bulk_attendance'),

    # Exam Type
    path('exam-types/', views.ExamTypeListView.as_view(), name='exam_type_list'),
    path('exam-types/add/', views.ExamTypeCreateView.as_view(), name='exam_type_create'),
    path('exam-types/<int:pk>/edit/', views.ExamTypeUpdateView.as_view(), name='exam_type_update'),
    path('exam-types/<int:pk>/delete/', views.ExamTypeDeleteView.as_view(), name='exam_type_delete'),

    # Exam
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/add/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('exams/<int:pk>/edit/', views.ExamUpdateView.as_view(), name='exam_update'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),

    # Exam Result
    path('exam-results/', views.ExamResultListView.as_view(), name='exam_result_list'),
    path('exam-results/add/', views.ExamResultCreateView.as_view(), name='exam_result_create'),
    path('exam-results/<int:pk>/edit/', views.ExamResultUpdateView.as_view(), name='exam_result_update'),
    path('exam-results/<int:pk>/delete/', views.ExamResultDeleteView.as_view(), name='exam_result_delete'),
    path('exam-results/bulk/', views.bulk_exam_result, name='bulk_exam_result'),

    # Fee Type
    path('fee-types/', views.FeeTypeListView.as_view(), name='fee_type_list'),
    path('fee-types/add/', views.FeeTypeCreateView.as_view(), name='fee_type_create'),
    path('fee-types/<int:pk>/edit/', views.FeeTypeUpdateView.as_view(), name='fee_type_update'),
    path('fee-types/<int:pk>/delete/', views.FeeTypeDeleteView.as_view(), name='fee_type_delete'),

    # Fee Structure
    path('fee-structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('fee-structures/add/', views.FeeStructureCreateView.as_view(), name='fee_structure_create'),
    path('fee-structures/<int:pk>/edit/', views.FeeStructureUpdateView.as_view(), name='fee_structure_update'),
    path('fee-structures/<int:pk>/delete/', views.FeeStructureDeleteView.as_view(), name='fee_structure_delete'),

    # Fee Payment
    path('fee-payments/', views.FeePaymentListView.as_view(), name='fee_payment_list'),
    path('fee-payments/add/', views.FeePaymentCreateView.as_view(), name='fee_payment_create'),
    path('fee-payments/<int:pk>/', views.FeePaymentDetailView.as_view(), name='fee_payment_detail'),
    path('fee-payments/<int:pk>/edit/', views.FeePaymentUpdateView.as_view(), name='fee_payment_update'),
    path('fee-payments/<int:pk>/delete/', views.FeePaymentDeleteView.as_view(), name='fee_payment_delete'),
    path('fee-payments/<int:pk>/receipt/', views.fee_payment_receipt, name='fee_payment_receipt'),

    # Promotion
    path('promotions/', views.PromotionListView.as_view(), name='promotion_list'),
    path('promotions/add/', views.PromotionCreateView.as_view(), name='promotion_create'),
    path('promotions/<int:pk>/edit/', views.PromotionUpdateView.as_view(), name='promotion_update'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion_delete'),
    path('promotions/bulk/', views.bulk_promotion, name='bulk_promotion'),

    # Timetable
    path('timetables/', views.TimetableListView.as_view(), name='timetable_list'),
    path('timetables/add/', views.TimetableCreateView.as_view(), name='timetable_create'),
    path('timetables/<int:pk>/edit/', views.TimetableUpdateView.as_view(), name='timetable_update'),
    path('timetables/<int:pk>/delete/', views.TimetableDeleteView.as_view(), name='timetable_delete'),

    # Notice
    path('notices/', views.NoticeListView.as_view(), name='notice_list'),
    path('notices/add/', views.NoticeCreateView.as_view(), name='notice_create'),
    path('notices/<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('notices/<int:pk>/edit/', views.NoticeUpdateView.as_view(), name='notice_update'),
    path('notices/<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice_delete'),

    # Event
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/add/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # Library Book
    path('library-books/', views.LibraryBookListView.as_view(), name='library_book_list'),
    path('library-books/add/', views.LibraryBookCreateView.as_view(), name='library_book_create'),
    path('library-books/<int:pk>/', views.LibraryBookDetailView.as_view(), name='library_book_detail'),
    path('library-books/<int:pk>/edit/', views.LibraryBookUpdateView.as_view(), name='library_book_update'),
    path('library-books/<int:pk>/delete/', views.LibraryBookDeleteView.as_view(), name='library_book_delete'),

    # Book Issue
    path('book-issues/', views.BookIssueListView.as_view(), name='book_issue_list'),
    path('book-issues/add/', views.BookIssueCreateView.as_view(), name='book_issue_create'),
    path('book-issues/<int:pk>/edit/', views.BookIssueUpdateView.as_view(), name='book_issue_update'),
    path('book-issues/<int:pk>/delete/', views.BookIssueDeleteView.as_view(), name='book_issue_delete'),

    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/attendance/', views.attendance_report, name='attendance_report'),
    path('reports/exam-results/', views.exam_results_report, name='exam_results_report'),
    path('reports/fee-collection/', views.fee_collection_report, name='fee_collection_report'),
    path('reports/student-progress/<int:student_id>/', views.student_progress_report, name='student_progress_report'),
]