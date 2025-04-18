from django.apps import AppConfig
class StudentAppConfig(AppConfig):
    name = 'student_app'

    def ready(self):
        import student_app.signals