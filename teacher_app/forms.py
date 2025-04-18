# teacher_app/forms.py


from django import forms
from django.contrib.auth.models import User

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import SpecialAttendance, Student

class SpecialAttendanceForm(forms.ModelForm):
    class Meta:
        model = SpecialAttendance
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SpecialAttendanceForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.all()
