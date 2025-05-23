# Generated by Django 5.1.7 on 2025-04-14 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0015_rename_division_teacher_class_division_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialattendance',
            name='semester',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='specialattendance',
            name='month',
            field=models.CharField(choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], default='01', max_length=2),
        ),
    ]
