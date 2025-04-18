from django.urls import path
from . import views as student_views

app_name = 'student_app'  # Unique app name for student-related URLs

urlpatterns = [
    path('', student_views.home, name='home'),
    path('student/login/', student_views.student_login, name='student_login'),
    path('student/dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('student/attendance-data/', student_views.student_attendance_data, name='student_attendance_data'),
    path('student/assessment-data/', student_views.student_assessment_data, name='student_assessment_data'),  # Updated path
    path('student/view-attendance/', student_views.student_view_attendance, name='view_attendance'),
    path('logout/', student_views.logout_view, name='logout'),
]
