from django.shortcuts import redirect
from .models import Teacher

def get_logged_in_teacher(request):
    """
    This function retrieves the currently logged-in teacher using the session.
    If no teacher is logged in, it redirects to the login page.
    """
    # Retrieve the teacher ID stored in the session
    teacher_id = request.session.get('teacher_id')

    # If no teacher ID in the session, redirect to the login page
    if not teacher_id:
        return None, redirect('teacher_login')
    
    # Try to fetch the teacher object from the database
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        return teacher, None
    except Teacher.DoesNotExist:
        # If the teacher does not exist in the database, redirect to the login page
        return None, redirect('teacher_login')
