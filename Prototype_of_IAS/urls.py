from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher/', include('teacher_app.urls')),  # Teacher app URLs
    path('student/', include('student_app.urls', namespace='student')),  # Correctly set the namespace for student
    path('', include('student_app.urls')),  # This should also have the correct namespace
]
