from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10, unique=True)  # Unique roll number for each student
    division = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date} - {self.get_status_display()}"

    @staticmethod
    def get_attendance_percentage(student, subject, month=None):
        """
        Calculate the attendance percentage for a student in a specific subject.
        Optionally, filter by month.
        """
        if month:
            total_classes = AttendanceRecord.objects.filter(student=student, subject=subject, date__month=month).count()
            present_classes = AttendanceRecord.objects.filter(student=student, subject=subject, status='Present', date__month=month).count()
        else:
            total_classes = AttendanceRecord.objects.filter(student=student, subject=subject).count()
            present_classes = AttendanceRecord.objects.filter(student=student, subject=subject, status='Present').count()

        if total_classes == 0:
            return 0
        return (present_classes / total_classes) * 100


class SpecialAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    lectures_attended = models.PositiveIntegerField()
    total_lectures = models.PositiveIntegerField()

class Assessment(models.Model):
    ASSESSMENT_CHOICES = [
        ('Pre-requisite Marks', 'Pre-requisite Marks'),
        ('Unit Test 1 Marks', 'Unit Test 1 Marks'),
        ('Unit Test 2 Marks', 'Unit Test 2 Marks'),
        ('Unit Test 3 Marks', 'Unit Test 3 Marks'),
        ('Insem Marks', 'Insem Marks'),
        ('Practical Marks', 'Practical Marks'),
        ('Oral Marks', 'Oral Marks'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_assessments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Ensure ForeignKey to Subject
    assessment_type = models.CharField(max_length=50, choices=ASSESSMENT_CHOICES)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.assessment_type} - {self.marks}"

class TotalAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lectures_attended = models.PositiveIntegerField()
    total_lectures = models.PositiveIntegerField()

    @property
    def attendance_percentage(self):
        if self.total_lectures > 0:
            return round((self.lectures_attended / self.total_lectures) * 100, 2)
        return 0.00
    
    def save(self, *args, **kwargs):
        if self.total_lectures > 0:
            self.attendance_percentage = (self.lectures_attended / self.total_lectures) * 100
        else:
            self.attendance_percentage = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.attendance_percentage:.2f}%"
