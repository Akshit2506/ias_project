from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, Teacher, Subject, AttendanceRecord, SpecialAttendance, Assessment, GenerateReport
from datetime import date
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from django.utils.timezone import now
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import CustomLoginForm
from django.urls import reverse
from reportlab.lib.pagesizes import letter

def teacher_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        print("Form submitted data:", request.POST)  # Debugging
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()

            print(f"Attempting login with username: {username} and password: {password}")  # Debugging

            # Custom authentication logic
            try:
                teacher = Teacher.objects.get(name=username, class_division=password)
                request.session['teacher_id'] = teacher.id  # Storing teacher id in session
                print(f"Teacher logged in successfully with ID: {teacher.id}")  # Debugging
                messages.success(request, "Logged in successfully!")
                return redirect('teacher:dashboard')  # Make sure 'teacher:dashboard' is correct
            except Teacher.DoesNotExist:
                print("❌ Teacher not found in DB or incorrect credentials.")  # Debugging
                messages.error(request, 'Invalid login credentials.')
        else:
            print("❌ Form is invalid.")  # Debugging
            print(form.errors)  # Print form errors for debugging
            messages.error(request, 'Please fix the errors in the form.')
    else:
        form = CustomLoginForm()

    return render(request, 'teacher/login.html', {'form': form})


# Teacher Dashboard View
def teacher_dashboard(request):
    teacher_id = request.session.get('teacher_id')
    print("🔍 Session teacher_id:", teacher_id)  # Debug print — ye terminal me dekhna

    if not teacher_id:
        messages.error(request, 'Please log in first.')
        print("🚫 No teacher_id in session. Redirecting to login.")
        return redirect('teacher:teacher_login')

    try:
        teacher = Teacher.objects.get(id=teacher_id)
        print("✅ Teacher found:", teacher.name)  # Ye bhi terminal me print hoga
        students = Student.objects.filter(division=teacher.class_division)
        subjects = Subject.objects.filter(teacher=teacher)
        context = {
        'teacher': teacher,
        'students': students,
        'subjects': subjects,
    }

        return render(request, 'teacher/teacher_dashboard.html', {
            'teacher': teacher,
            'students': students,
            'subjects': subjects
        })
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher not found.')
        print("❌ Teacher not found with ID:", teacher_id)
        return redirect('teacher:teacher_login')


# Teacher Logout
def teacher_logout(request):
    try:
        del request.session['teacher_id']  # Remove the teacher's session
        messages.success(request, 'You have logged out successfully.')
    except KeyError:
        pass  # If there's no teacher logged in, nothing to delete
    
    return redirect('teacher:teacher_login')  # Redirect to login page after logout

## -------------------- Mark Attendance --------------------
def mark_attendance(request):
    students = Student.objects.all()  # All students
    subjects = Subject.objects.all()  # All subjects

    selected_date = request.POST.get('attendance_date', '')  # Selected date from the form
    selected_subject = request.POST.get('subject', '')  # Selected subject from the form

    attendance_summary = []  # Attendance summary ke liye empty list

    if request.method == 'POST' and selected_date and selected_subject:
        subject_id = int(selected_subject)
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()  # Convert the string date to a datetime object
        
        # Filter AttendanceRecord based on subject and date
        filtered_attendance = AttendanceRecord.objects.filter(
            subject_id=subject_id,
            date=selected_date
        )

        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                AttendanceRecord.objects.create(
                    student=student,
                    subject_id=subject_id,
                    status=status,
                    date=selected_date,
                )

        return redirect('teacher:teacher_login')  # 🔁 Updated redirect to match correct URL name

    context = {
        'students': students,
        'subjects': subjects,
        'selected_date': selected_date,
        'selected_subject': selected_subject,
        'attendance_summary': attendance_summary,
    }

    return render(request, 'teacher/mark_attendance.html', context)


# -------------------- Manual Attendance Summary --------------------
def manual_attendance_summary(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()

    attendance_summary = []

    if request.method == 'POST':
        selected_subject = request.POST.get('subject')
        selected_month = request.POST.get('month')

        if selected_subject and selected_month:
            subject_id = int(selected_subject)
            month = int(selected_month)
            filtered_attendance = AttendanceRecord.objects.filter(
                subject_id=subject_id,
                date__month=month
            )

            for student in students:
                student_records = filtered_attendance.filter(student=student)
                total = student_records.count()
                present = student_records.filter(status="Present").count()
                percentage = (present / total) * 100 if total > 0 else 0
                attendance_summary.append({
                    'student': student,
                    'present': present,
                    'total': total,
                    'percentage': percentage
                })

    months = [
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ]

    context = {
        'students': students,
        'subjects': subjects,
        'months': months,
        'attendance_summary': attendance_summary,
    }

    return render(request, 'teacher/manual_attendance_summary.html', context)

# -------------------- Special Attendance --------------------
# Keep this version — properly defined once
def special_attendance(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher:teacher_login')

    teacher = Teacher.objects.get(id=teacher_id)
    subjects = Subject.objects.filter(teacher=teacher)
    students = Student.objects.filter(division=teacher.class_division)

    months = [
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ]

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')

        try:
            subject = Subject.objects.get(id=subject_id)
            student = Student.objects.get(id=student_id)

            for i in range(1, 5):
                month = request.POST.get(f'month_{i}')
                attended = request.POST.get(f'attended_{i}')
                total = request.POST.get(f'total_{i}')

                if month and attended and total:
                    SpecialAttendance.objects.create(
                        student=student,
                        subject=subject,
                        month=month,
                        semester=i,
                        lectures_attended=attended,
                        total_lectures=total
                    )

            return redirect('teacher:special_attendance')

        except Exception as e:
            print(f"Error: {e}")
            return redirect('teacher:special_attendance')

    return render(request, 'teacher/special_attendance.html', {
        'teacher': teacher,
        'subjects': subjects,
        'students': students,
        'months': [m[1] for m in months],
        'is_special_attendance': True,
    })

def upload_assessment(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher:teacher_login')

    teacher = Teacher.objects.get(id=teacher_id)
    students = Student.objects.filter(division=teacher.class_division)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        print("🔥 Received POST request at /upload-assessment/")
        print("📦 POST Data:", request.POST)

        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')

        print(f"📌 Selected Subject ID: {subject_id}, Student ID: {student_id}")

        try:
            subject = Subject.objects.get(id=subject_id)
            student = Student.objects.get(id=student_id)

            # Fetch marks from form using dynamic field names
            prerequisite = int(request.POST.get(f'prerequisite_{student.id}', 0))
            ut1 = int(request.POST.get(f'ut1_{student.id}', 0))
            ut2 = int(request.POST.get(f'ut2_{student.id}', 0))
            ut3 = int(request.POST.get(f'ut3_{student.id}', 0))
            insem = int(request.POST.get(f'insem_{student.id}', 0))
            pr_marks = int(request.POST.get(f'pr_marks_{student.id}', 0))
            or_marks = int(request.POST.get(f'or_marks_{student.id}', 0))

            print("✅ All marks received:")
            print(f"Prerequisite: {prerequisite}, UT1: {ut1}, UT2: {ut2}, UT3: {ut3}, Insem: {insem}, PR: {pr_marks}, OR: {or_marks}")

            # Create Assessment entry
            Assessment.objects.create(
                student=student,
                subject=subject,
                prerequisite=prerequisite,
                ut1=ut1,
                ut2=ut2,
                ut3=ut3,
                insem=insem,
                pr_marks=pr_marks,
                or_marks=or_marks,
            )

            messages.success(request, "✅ Assessment uploaded successfully.")
            print("🎯 Assessment saved in database.")
            return redirect('teacher:dashboard')  # Redirect to dashboard (NOT login)

        except (Subject.DoesNotExist, Student.DoesNotExist):
            messages.error(request, "❌ Invalid subject or student selected.")
            print("❌ Error: Subject or Student not found.")

        except Exception as e:
            messages.error(request, f"❌ Something went wrong: {str(e)}")
            print("❌ Exception occurred while uploading:", str(e))
            return redirect('teacher:upload_assessment')

    return render(request, 'teacher/upload_assessment.html', {
        'teacher': teacher,
        'students': students,
        'subjects': subjects,
    })


# -------------------- Generate Report --------------------
@transaction.atomic
def generate_report(request):
    # Get the selected student from the GET request
    student_id = request.GET.get('student')  # Get the selected student
    student = get_object_or_404(Student, id=student_id)  # Fetch student details
    
    # Example month, you can replace this with actual logic
    month = "April"
    
    # Call the existing report generation logic (HTML to PDF)
    return generate_pdf_report(student, month)

def generate_pdf_report(student, month):
    template_path = 'teacher/report_template.html'
    context = {
        'student': student,
        'month': month,
        # Add more context data as required
    }

    # Generate HTML from the template
    template = get_template(template_path)
    html_content = template.render(context)
    
    # Convert HTML to PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{student.name}_report_{month}.pdf"'
        return response
    
    return HttpResponse("Error generating PDF", status=500)

def download_report_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)  # Get student by ID
    
    # Create a response with the appropriate PDF content-type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{student.name}.pdf"'

    # Generate the PDF document
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Basic details (You can add more if necessary)
    pdf.drawString(100, 800, f"Student Report for {student.name}")
    pdf.drawString(100, 780, f"Roll Number: {student.roll_number}")
    pdf.drawString(100, 760, f"Division: {student.division}")
    
    # Add Attendance Records
    pdf.drawString(100, 740, "Attendance Summary:")
    attendance_records = AttendanceRecord.objects.filter(student=student)
    for i, record in enumerate(attendance_records):
        pdf.drawString(100, 720 - i*20, f"Subject: {record.subject.name}, Status: {record.status}")
    
    # Add Assessment Marks
    pdf.drawString(100, 640, "Assessment Summary:")
    assessments = Assessment.objects.filter(student=student)
    for i, assessment in enumerate(assessments):
        pdf.drawString(100, 620 - i*20, f"Subject: {assessment.subject.name}, UT1: {assessment.ut1}, UT2: {assessment.ut2}")
    
    # Finalize and save the PDF
    pdf.showPage()
    pdf.save()

    # Get the PDF content and return as a response
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()

    return response