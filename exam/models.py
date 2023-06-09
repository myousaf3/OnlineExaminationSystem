from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=10,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    
    def __str__(self):  
        return self.user.first_name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Exam(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams_created')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    questions_count = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.subject.name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    question_text = models.TextField()
    question_type = models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('text_based', 'Text Based')], max_length=20)
    
    def __str__(self):
            return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=100,null=True, blank=True)
    option2 = models.CharField(max_length=100,null=True, blank=True)
    option3 = models.CharField(max_length=100,null=True, blank=True)
    option4 = models.CharField(max_length=100,null=True, blank=True)
    answer = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')],null=True, blank=True)
    
    def __str__(self):
            return self.question.question_text


class Attempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.exam.subject.name


class ApprovalRequest(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_requests')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='approval_requests')
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.exam.subject.name