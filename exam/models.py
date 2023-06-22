from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(
        choices=[("teacher", "Teacher"), ("student", "Student")],
        max_length=10,
    )
    profile_picture = CloudinaryField("image")

    def __str__(self):
        return self.user.first_name


class Subject(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Exam(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="exams_created", null=True
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, related_name="exams", null=True
    )
    start_time = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    end_time = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    is_approved = models.BooleanField(default=False)
    is_requested = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be greater than start time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True)
    score = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    question_text = models.TextField()
    question_type = models.CharField(
        choices=[("multiple_choice", "Multiple Choice"), ("text_based", "Text Based")],
        max_length=100,
    )

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=25, null=True)
    option2 = models.CharField(max_length=25, null=True)
    option3 = models.CharField(max_length=25, null=True)
    option4 = models.CharField(max_length=25, null=True)
    answer = models.IntegerField(
        choices=[(1, "Option 1"), (2, "Option 2"), (3, "Option 3"), (4, "Option 4")],
        null=True,
    )
    text_answer = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.question.question_text


class Attempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(default=0)
    is_attempted = models.BooleanField(default=False)

    def __str__(self):
        return self.exam.subject.name


class AttemptQuestion(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attempts", null=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=20, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.question_text


class ApprovalRequest(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="approval_requests"
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.exam.subject.name


class TempSessionScore(models.Model):
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.score}"
