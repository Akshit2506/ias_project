# add_subjects.py

from teacher_app.models import Subject  # Import your Subject model here

# List of subjects to add
subjects_data = [
    ("Software Engineering", "SE101"),
    ("Microprocessor", "MP102"),
    ("Data Structures and Algorithms", "DSA103"),
    ("Principles of Programming Languages", "PPL104"),
    ("Engineering Mathematics - III", "EMT305"),
]

# Insert subjects into the database
for subject_name, subject_code in subjects_data:
    Subject.objects.create(name=subject_name, code=subject_code)

print("Subjects added successfully.")
