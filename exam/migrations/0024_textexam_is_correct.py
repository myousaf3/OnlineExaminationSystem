# Generated by Django 4.2.2 on 2023-06-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0023_alter_profile_profile_picture_textexam"),
    ]

    operations = [
        migrations.AddField(
            model_name="textexam",
            name="is_correct",
            field=models.BooleanField(default=False),
        ),
    ]
