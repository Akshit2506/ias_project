from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Subject, AttendanceRecord, SpecialAttendance, Assessment
from django.db.models import Count
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.urls import reverse
from collections import defaultdict
from teacher_app.models import SpecialAttendance
from student_app.models import Student, TotalAttendance

def home(request):
    return render(request, 'student/home.html', {
        'student_login_url': reverse('student_app:student_login'),  # Updated to match the new namespace
    })

def student_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')

        try:
            student = Student.objects.get(name=name, roll_number=roll_number)
            request.session['student_id'] = student.id  # Save student ID in session
            return redirect('student_app:student_dashboard')  # Updated namespace
        except Student.DoesNotExist:
            messages.error(request, 'Invalid name or roll number.')
            return render(request, 'student/student_login.html')

    return render(request, 'student/student_login.html')  # ✅ Yeh fix tha

def student_dashboard(request):
    print("Student Dashboard is called")
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_app:student_login')  # Updated namespace

    student = Student.objects.get(id=student_id)
    attendance = TotalAttendance.objects.filter(student=student)  # Fetch student attendance data
    assessments = Assessment.objects.filter(student=student)  # Fetch student assessments data
    
    context = {
        'student': student,
        'attendance': attendance,
        'assessments': assessments,
    }
    return render(request, 'student/student_dashboard.html', {'student': student})

def student_view_attendance(request):
    # Simulating logged-in student (Replace with actual session-based student data later)
    student = {
        'name': 'Akshit Somkure',
        'roll_number': '2',
        'division': 'A',
    }

    # Hardcoded attendance data (Later replace with actual DB queries)
    final_attendance_by_subject = {
        'Software Engineering': 49.11,
        'Engineering Mathematics III': 49.11,
        'Principles of Programming Languages': 45.95,
        'Data Structures and Algorithms': 47.27,
        'Microprocessor': 50.0,
    }

    # Calculate final average attendance
    final_average_attendance = sum(final_attendance_by_subject.values()) / len(final_attendance_by_subject)

    # Pass data to template for rendering
    context = {
        'student': student,
        'final_attendance_by_subject': final_attendance_by_subject,
        'final_average_attendance': round(final_average_attendance, 2),
    }

    return render(request, 'student/view_attendance.html', context)

def student_attendance_data(request):
    # Static Data (jo tumne diya)
    attendance_data = {
        'student_name': 'Akshit Somkure',
        'roll_number': '02',
        'division': 'A',
        'subject': 'Software Engineering',
        'attendance': {
            'Jan': {'attended': 15, 'total': 30},
            'Feb': {'attended': 16, 'total': 28},
            'Mar': {'attended': 15, 'total': 30},
            'Apr': {'attended': 14, 'total': 31},
        }
    }

    # Select subject for static data
    selected_subject = attendance_data['subject']

    # Choose a month (static for now, but you can make it dynamic)
    month = 'Mar'  # Example: March
    
    # Calculate total and attended lectures for the month
    total_lectures = attendance_data['attendance'][month]['total']
    attended_lectures = attendance_data['attendance'][month]['attended']

    # Calculate attendance percentage
    if total_lectures > 0:
        attendance_percentage = (attended_lectures / total_lectures) * 100
    else:
        attendance_percentage = 0.0

    # Debug: Print the data to see if everything is correct
    print("Context data being passed:")
    print({
        'student': attendance_data,
        'subjects': [attendance_data['subject']],  # For static data, just show this subject
        'selected_subject': selected_subject,
        'month': month,
        'total_lectures': total_lectures,
        'attended_lectures': attended_lectures,
        'attendance_percentage': attendance_percentage,
    })

    return render(request, 'student/student_attendance.html', {
        'student': attendance_data,
        'subjects': [attendance_data['subject']],  # For static data, just show this subject
        'selected_subject': selected_subject,
        'month': month,
        'total_lectures': total_lectures,
        'attended_lectures': attended_lectures,
        'attendance_percentage': attendance_percentage,
    })

def student_assessment_data(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    assessments = Assessment.objects.filter(student_id=student_id)

    assessment_data = {}
    for assessment in assessments:
        subject_name = assessment.subject.name
        if subject_name not in assessment_data:
            assessment_data[subject_name] = []
        assessment_data[subject_name].append({
            'assessment_type': assessment.assessment_type,
            'marks': assessment.marks,
        })

    return JsonResponse({'assessment': assessment_data})
# ✅ Utility function for DRY code
def get_logged_in_student(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return None
    try:
        return Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return None

from django.shortcuts import redirect

def logout_view(request):
    # Clear session data or logout logic
    request.session.flush()
    return redirect('student_app:student_login')  # Updated namespace
