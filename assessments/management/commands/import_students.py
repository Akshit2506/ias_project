import csv
import os
from django.core.management.base import BaseCommand
from assessments.models import Student  # Apne model ka import check karo

class Command(BaseCommand):
    help = "Import students from a CSV file"

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(os.getcwd(), "students.csv")  # Ensure correct path
        
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row["name"]
                    roll_number = row["roll_number"]

                    student, created = Student.objects.get_or_create(
                        name=name, 
                        roll_number=roll_number
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Added: {name} ({roll_number})"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Already exists: {name} ({roll_number})"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("❌ students.csv file not found!"))
