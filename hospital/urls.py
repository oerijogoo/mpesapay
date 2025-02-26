from django.urls import path
from django.contrib.auth import views as auth_views
from hospital import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.patient_register, name='patient_register'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('admit-patient/<int:patient_id>/', views.admit_patient, name='admit_patient'),
    path('patient/book-appointment/', views.patient_book_appointment, name='patient_book_appointment'),
    path('receptionist/book-appointment/', views.receptionist_book_appointment, name='receptionist_book_appointment'),
    path('doctor/book-appointment/', views.doctor_book_appointment, name='doctor_book_appointment'),
    path('kiosk/book-appointment/', views.kiosk_book_appointment, name='kiosk_book_appointment'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='hospital/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='hospital/logout.html'), name='logout'),

    # Dashboard Redirect
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]