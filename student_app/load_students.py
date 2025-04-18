import os
import pandas as pd
from student_app.models import Student

file_path = r"C:\Users\akshi\OneDrive\Desktop\Prototype_of_IAS\Prototype_of_IAS\students.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df.rename(columns={"Student's Name": "name", "Roll No.": "roll_no"}, inplace=True)

    students_to_insert = [
        Student(name=row["name"], roll_no=int(row["roll_no"]))
        for _, row in df.iterrows()
    ]

    Student.objects.bulk_create(students_to_insert)
    print("✅ Data Successfully Inserted!")
else:
    print("❌ File Not Found! Check the path.")
