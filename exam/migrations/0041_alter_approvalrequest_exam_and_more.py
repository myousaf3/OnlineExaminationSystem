# Generated by Django 4.2.2 on 2023-06-20 08:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0040_alter_subject_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approvalrequest",
            name="exam",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="apprequests",
                to="exam.exam",
            ),
        ),
        migrations.AlterField(
            model_name="attemptquestion",
            name="selected_option",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="text_answer",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="score",
            field=models.PositiveIntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="tempsessionscore",
            name="score",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
