# Generated by Django 4.2.2 on 2023-06-19 18:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0039_alter_approvalrequest_exam_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="name",
            field=models.CharField(max_length=25),
        ),
    ]
