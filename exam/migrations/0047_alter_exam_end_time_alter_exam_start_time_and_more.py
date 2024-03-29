# Generated by Django 4.2.2 on 2023-06-21 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exam", "0046_alter_exam_end_time_alter_exam_start_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exam",
            name="end_time",
            field=models.DateTimeField(default="2023-06-21 08:39"),
        ),
        migrations.AlterField(
            model_name="exam",
            name="start_time",
            field=models.DateTimeField(default="2023-06-21 08:39"),
        ),
        migrations.AlterField(
            model_name="exam",
            name="subject",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="exams",
                to="exam.subject",
            ),
        ),
        migrations.AlterField(
            model_name="exam",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="exams_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
