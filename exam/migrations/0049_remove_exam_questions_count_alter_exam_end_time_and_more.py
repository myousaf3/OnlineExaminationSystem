# Generated by Django 4.2.2 on 2023-06-21 09:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0048_alter_attempt_score_alter_attempt_student_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exam",
            name="questions_count",
        ),
        migrations.AlterField(
            model_name="exam",
            name="end_time",
            field=models.DateTimeField(default="2023-06-21 09:09"),
        ),
        migrations.AlterField(
            model_name="exam",
            name="start_time",
            field=models.DateTimeField(default="2023-06-21 09:09"),
        ),
    ]
