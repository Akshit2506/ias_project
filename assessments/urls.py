from django.urls import path
from student_app.views import student_dashboard
from teacher_app.views import teacher_dashboard
from . import views  # optional, only if this file has any views (usually not needed)

urlpatterns = [
    # ✅ You can add this only if home_view and login_view exist
    # path('', home_view, name='home'),
    # path('student/login/', login_view, name='student_login'),

    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
]
