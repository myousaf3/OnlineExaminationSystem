# Generated by Django 4.2.2 on 2023-06-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0025_textexam_score_alter_option_answer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="answer",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "Option 1"),
                    (2, "Option 2"),
                    (3, "Option 3"),
                    (4, "Option 4"),
                ],
                null=True,
            ),
        ),
    ]