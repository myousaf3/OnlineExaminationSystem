# Generated by Django 4.2.2 on 2023-06-14 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0016_rename_tempscore_tempsessionscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.subject'),
        ),
    ]
