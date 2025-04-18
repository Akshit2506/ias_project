from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('special-attendance/', views.special_attendance, name='special_attendance'),
    path('upload-assessment/', views.upload_assessment, name='upload_assessment'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    
    # Updated the path to include student_id in generate_report URL
    path('generate-report/<int:student_id>/', views.generate_report, name='generate_report'),
    
    # Keep the download_report path as is
    path('teacher/download_report/<int:student_id>/', views.download_report_pdf, name='download_report_pdf'),
]
