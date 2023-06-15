from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Option, Exam


class SignUpForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ('first_name','last_name','username', 
                'email', 'password1', 'password2')

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class ExamSubmissionForm(forms.Form):
    question_answers = forms.MultipleChoiceField()
    

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'question_text','score']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option1', 'option2', 'option3', 'option4', 'answer']
        
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
