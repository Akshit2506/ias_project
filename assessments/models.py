from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)  # Unique roll number (acts as password)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

# ✅ अब Teacher model add किया
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)  # Class division को password की तरह use करेंगे

    def __str__(self):
        return f"{self.name}"
