# Generated by Django 4.2.2 on 2023-06-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_exam_is_requested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attempt',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='attempt',
            name='start_time',
        ),
        migrations.AddField(
            model_name='exam',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
