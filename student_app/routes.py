from django.urls import path
from . import views  # Ensure correct import

urlpatterns = [
    path('login/', views.student_login, name='student_login'),  # Fix function name
]
