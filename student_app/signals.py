# student_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from teacher_app.models import SpecialAttendance
from student_app.models import TotalAttendance

@receiver(post_save, sender=SpecialAttendance)
def update_total_attendance(sender, instance, created, **kwargs):
    if created:
        student = instance.student
        subject = instance.subject.name
        attended = instance.lectures_attended
        total = instance.total_lectures

        total_attendance, _ = TotalAttendance.objects.get_or_create(
            student=student,
            subject=subject
        )

        total_attendance.lectures_attended += attended
        total_attendance.total_lectures += total
        total_attendance.save()
