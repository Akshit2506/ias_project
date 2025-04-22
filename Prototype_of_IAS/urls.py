from django.contrib import admin
from django.urls import path, include
from student_app import views as student_views  # ✅ Add this line

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher/', include('teacher_app.urls')),
    path('student/', include('student_app.urls', namespace='student')),
    path('', student_views.home, name='root_home'),  # ✅ Now this will work
]
