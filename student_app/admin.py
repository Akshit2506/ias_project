from django.contrib import admin
from django.shortcuts import render
from .models import Student, TotalAttendance, Assessment, Subject  # Import your models
from django.contrib.auth.decorators import login_required
# Registering the Student model using decorator
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin panel
    list_display = ('name', 'roll_number', 'division')
    
    # Fields to be displayed in the form for adding/editing a student
    fields = ('name', 'roll_number', 'division')
    
    # Adding search functionality to search by name or roll_number
    search_fields = ('name', 'roll_number')
    
    # Adding filter options by division
    list_filter = ('division',)
    
    # Ordering the student list by name
    ordering = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

# Registering the TotalAttendance model
@admin.register(TotalAttendance)
class TotalAttendanceAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ['student', 'subject', 'lectures_attended', 'total_lectures', 'attendance_percentage']
    
    # Add a search bar for easy filtering
    search_fields = ('student__name', 'subject__name')
    
    # Adding filter options for subjects and students
    list_filter = ('subject', 'student')

# Registering the Assessment model
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'assessment_type', 'marks']  # Add subject in list_display
    list_filter = ['subject', 'assessment_type']  # Add subject for filtering
    search_fields = ['student__name', 'subject__name']  # Search by subject as well
    ordering = ['student']

@login_required(login_url='student:student_login')  # Redirects to login if not authenticated
def attendance_data(request):
    # Assuming you're using the logged-in user to get student data
    student = request.user.student  # Make sure user has a related student profile
    attendance = TotalAttendance.objects.filter(student=student)

    return render(request, 'student/attendance_data.html', {'attendance': attendance})