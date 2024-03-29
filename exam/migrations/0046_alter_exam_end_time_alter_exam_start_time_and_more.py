# Generated by Django 4.2.2 on 2023-06-21 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exam", "0045_alter_attempt_exam_alter_attempt_score_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exam",
            name="end_time",
            field=models.DateTimeField(default="2023-06-21 08:29"),
        ),
        migrations.AlterField(
            model_name="exam",
            name="start_time",
            field=models.DateTimeField(default="2023-06-21 08:29"),
        ),
        migrations.AlterField(
            model_name="exam",
            name="subject",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exams",
                to="exam.subject",
            ),
        ),
        migrations.AlterField(
            model_name="exam",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exams_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
