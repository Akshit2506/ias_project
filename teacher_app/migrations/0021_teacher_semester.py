# Generated by Django 5.2 on 2025-04-21 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0020_remove_teacher_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='semester',
            field=models.CharField(default='SE', max_length=100),
            preserve_default=False,
        ),
    ]
