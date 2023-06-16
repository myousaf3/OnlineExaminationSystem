from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ("Admin", "Admin"),
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES, max_length=10, null=True, blank=True
    )
    profile_picture = CloudinaryField("image")

    def __str__(self):
        return self.user.first_name


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exam(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="exams_created"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exams")
    questions_count = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_requested = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.subject.name

    def update_visibility(self):
        now = timezone.now()
        if self.is_approved and self.start_time > now:
            self.is_visible = True

    def save(self, *args, **kwargs):
        self.update_visibility()
        super().save(*args, **kwargs)


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True
    )
    score = models.PositiveIntegerField(null=True, blank=True)
    question_text = models.TextField()
    question_type = models.CharField(
        choices=[("multiple_choice", "Multiple Choice"), ("text_based", "Text Based")],
        max_length=20,
    )

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=100, null=True, blank=True)
    option2 = models.CharField(max_length=100, null=True, blank=True)
    option3 = models.CharField(max_length=100, null=True, blank=True)
    option4 = models.CharField(max_length=100, null=True, blank=True)
    answer = models.IntegerField(
        choices=[(1, "Option 1"), (2, "Option 2"), (3, "Option 3"), (4, "Option 4")],
        null=True,
        blank=True,
    )
    text_answer = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.question.question_text


class Attempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(null=True, blank=True)
    is_attempted = models.BooleanField(default=False)

    def __str__(self):
        return self.exam.subject.name


class AttemptQuestion(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attempts", null=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=100, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.question_text


class ApprovalRequest(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="approval_requests"
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="approval_requests"
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.exam.subject.name


class TempSessionScore(models.Model):
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.score}"
