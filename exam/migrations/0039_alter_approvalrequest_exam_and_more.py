# Generated by Django 4.2.2 on 2023-06-19 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0038_alter_attemptquestion_selected_option_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approvalrequest",
            name="exam",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="approval_requests",
                to="exam.exam",
            ),
        ),
        migrations.AlterField(
            model_name="attemptquestion",
            name="selected_option",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option1",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option2",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option3",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option4",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="text_answer",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_type",
            field=models.CharField(
                choices=[
                    ("multiple_choice", "Multiple Choice"),
                    ("text_based", "Text Based"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="score",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="subject",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="tempsessionscore",
            name="score",
            field=models.PositiveIntegerField(),
        ),
    ]
