# Generated by Django 4.2.2 on 2023-06-12 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0011_remove_attempt_end_time_remove_attempt_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
