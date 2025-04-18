from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def teacher_login(request):
    return render(request, 'teacher_login.html')

def student_login(request):
    return render(request, 'student_login.html')