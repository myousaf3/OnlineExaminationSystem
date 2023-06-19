from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Option, Exam
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user_type", "profile_picture"]

    user_type = forms.ChoiceField(
        choices=[("teacher", "Teacher"), ("student", "Student")],
        widget=forms.RadioSelect,
    )

    profile_picture = forms.ImageField()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class GroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class ExamSubmissionForm(forms.Form):
    question_answers = forms.MultipleChoiceField()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["exam", "question_text", "score"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option1", "option2", "option3", "option4", "answer"]


class TextForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text_answer"]


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["subject", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
