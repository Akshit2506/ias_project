from django.contrib import admin
from .models import Teacher, Student, Subject, AttendanceRecord, SpecialAttendance, Assessment, GenerateReport
from .forms import SpecialAttendanceForm
from django import forms

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_division')
    search_fields = ['name', 'class_division']  # Allow searching by teacher's name or class division

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status')
    list_filter = ('status', 'subject', 'date')
    search_fields = ('student__name', 'subject__name')
    list_per_page = 20
    date_hierarchy = 'date'


class SpecialAttendanceAdmin(admin.ModelAdmin):
    # List display should only refer to valid model fields
    list_display = ('student', 'subject', 'month', 'lectures_attended', 'total_lectures', 'semester', 'remarks', 'extra_option_1', 'extra_option_2', 'extra_option_3')

    # Only valid fields should be listed in list_filter
    list_filter = ('subject', 'month', 'semester', 'extra_option_1', 'extra_option_2', 'extra_option_3')

    # Enable searching for valid fields
    search_fields = ('student__name', 'subject__name', 'remarks')

    # Define how the fields will be grouped in the admin form
    fieldsets = (
        (None, {
            'fields': ('student', 'subject', 'month', 'lectures_attended', 'total_lectures', 'semester')
        }),
        ('Special Attendance Options', {
            'fields': ('remarks', 'extra_option_1', 'extra_option_2', 'extra_option_3')
        }),
    )

admin.site.register(SpecialAttendance, SpecialAttendanceAdmin)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'prerequisite', 'ut1', 'ut2', 'ut3', 'insem', 'pr_marks', 'or_marks', 'created_at')
    search_fields = ['student__name', 'subject__name']
    list_filter = ('subject',)


   

class GenerateReportForm(forms.ModelForm):
    class Meta:
        model = GenerateReport
        # Exclude the non-editable field from the form
        fields = ['teacher', 'student', 'total_attendance', 'special_attendance', 'assessment']
        # Alternatively, you can use exclude like this:
        # exclude = ['report_generated_at']

 
@admin.register(GenerateReport)
class GenerateReportAdmin(admin.ModelAdmin):
    form = GenerateReportForm  # Use the custom form
    list_display = ('teacher', 'student', 'total_attendance', 'report_generated_at')
    list_filter = ('teacher', 'student')
    search_fields = ('teacher__name', 'student__name')
    date_hierarchy = 'report_generated_at'
    ordering = ('-report_generated_at',)
    list_display_links = ('teacher', 'student')