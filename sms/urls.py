from django.urls import path
from . import views

urlpatterns = [
    # html urls
    path('', views.student_list, name='student_list'),
    path('sms/<int:pk>/', views.student_detail, name='student_detail'),
    path('add/', views.student_create, name='student_create'),
    path('sms/<int:pk>/edit/', views.student_update, name='student_update'),
    path('sms/<int:pk>/delete/', views.student_delete, name='student_delete'),
    # api urls
    path('api/sms/', views.student_list_api, name='student_list_api'),
    path('api/sms/<int:pk>/', views.student_detail_api, name='student_detail_api'),
]
