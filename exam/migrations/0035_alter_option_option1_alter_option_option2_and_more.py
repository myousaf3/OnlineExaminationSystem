# Generated by Django 4.2.2 on 2023-06-19 18:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exam", "0034_alter_option_option1_alter_option_option2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="option1",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option2",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option3",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="option4",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="option",
            name="text_answer",
            field=models.CharField(max_length=15, null=True),
        ),
    ]
