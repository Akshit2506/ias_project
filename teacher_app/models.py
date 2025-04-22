from django.db import models
from django.core.exceptions import ValidationError
from student_app.models import Student
from django.db.models import Count, Q

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    class_division = models.CharField(max_length=10)  # e.g. SE-A
    password = models.CharField(max_length=100)  # use hashing later for security
    semester = models.CharField(max_length=100)  # ✅ Now it will accept strings like "Software Engineering"

    def __str__(self):
        return f"{self.name} ({self.class_division})"

class Subject(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.teacher.name})"


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='teacher_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date = models.DateField()

    @staticmethod
    def get_attendance_summary(subject, month):
        records = AttendanceRecord.objects.filter(subject=subject, date__month=month)

        if not records.exists():
            return "No attendance records found for the given subject and month."

        attendance_summary = (
            records.values('student')
            .annotate(total=Count('id'), present=Count('id', filter=Q(status='Present')))
        )

        for record in attendance_summary:
            record['percentage'] = (record['present'] / record['total']) * 100 if record['total'] > 0 else 0

        return attendance_summary



class SpecialAttendance(models.Model):
    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='teacher_special_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    month = models.CharField(max_length=2, choices=MONTH_CHOICES, default='01')  # Default to January
    lectures_attended = models.IntegerField()
    total_lectures = models.IntegerField()
    date_submitted = models.DateField(auto_now_add=True)
    semester = models.IntegerField()

    # Additional fields (for customization, if needed)
    remarks = models.TextField(blank=True, null=True)
    extra_option_1 = models.BooleanField(default=False)
    extra_option_2 = models.BooleanField(default=False)
    extra_option_3 = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.lectures_attended > self.total_lectures:
            raise ValueError("Lectures attended cannot be greater than total lectures")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {dict(self.MONTH_CHOICES).get(self.month)}"
    
class Assessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    prerequisite = models.IntegerField()
    ut1 = models.IntegerField()
    ut2 = models.IntegerField()
    ut3 = models.IntegerField()
    insem = models.IntegerField()
    pr_marks = models.IntegerField()
    or_marks = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        for field in ['prerequisite', 'ut1', 'ut2', 'ut3', 'insem', 'pr_marks', 'or_marks']:
            value = getattr(self, field)
            if not (0 <= value <= 100):
                raise ValidationError(f"{field} must be between 0 and 100")

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"
class GenerateReport(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_attendance = models.IntegerField()
    special_attendance = models.ForeignKey(SpecialAttendance, on_delete=models.SET_NULL, null=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.SET_NULL, null=True)
    report_generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.student.name} by {self.teacher.name}"

    @classmethod
    def generate_report_for_teacher(cls, teacher_division, month):
        teacher = Teacher.objects.filter(class_division=teacher_division).first()

        if teacher:
            # Prefetch the related student, attendance, special attendance, and assessment data
            students_in_division = Student.objects.filter(division=teacher.division).prefetch_related(
                'attendance',  # Assuming you have a related name or foreign key set up for attendance
                'special_attendance',  # Make sure this relationship is set properly
                'assessment'  # Same for assessments
            )

            for student in students_in_division:
                # Query attendance records for the student
                total_attendance = AttendanceRecord.objects.filter(student=student, date__month=month).count()

                # Fetch special attendance for the student
                special_attendance = student.special_attendance.filter(month=month).first()

                # Get the latest assessment (if available)
                assessment = student.assessment.latest('created_at') if student.assessment.exists() else None

                # Create the report
                cls.objects.create(
                    teacher=teacher,
                    student=student,
                    total_attendance=total_attendance,
                    special_attendance=special_attendance,
                    assessment=assessment
                )

            return "Reports generated successfully."
        else:
            return "Teacher with the given division not found."
