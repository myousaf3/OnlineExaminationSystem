from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserLoginForm, ExamSubmissionForm,QuestionForm, OptionForm
from exam.models import Question, Subject, User, Exam
from django.db.models import Q


def signup(request): 
    form = SignUpForm(request.POST) 
    if form.is_valid(): 
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password') 
        email = form.cleaned_data.get('email') 
        form.save() 
        user = authenticate(username=username, password=password) 
        login(request, user) 
        return redirect('/login')
    context = {     
        'form': form 
    } 
    return render(request, 'signup.html', context) 

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('exam_submission')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def exam_submission(request):
    subjects = Subject.objects.all()
    subject_count = Subject.objects.count() 
    student_count = User.objects.count() 
    question_count = Question.objects.count() 
    exams = Exam.objects.all() 
    questions = Question.objects.all()     
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_form = OptionForm(request.POST)
        if question_form.is_valid() and option_form.is_valid():
            question = question_form.save()
            option = option_form.save(commit=False)
            option.question = question
            option.save()
        # Do something after the data is saved
    else:
        question_form = QuestionForm()
        option_form = OptionForm()
    return render(request, 'exam_submission.html', {'question_form': question_form, 'option_form': option_form, 'subjects':subjects,'subject_count':subject_count,'student_count':student_count,'question_count':question_count,'exams':exams,'questions':questions})


def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    exam_pk = question.exam.pk  # get the pk of the related Exam instance
    question.delete()
    return redirect('/exam-submission/', pk=exam_pk)  # redirect the user to the related Exam detail view


@login_required(login_url='login')
def question_view(request,name):
    subject_count = Subject.objects.count() 
    student_count = User.objects.count() 
    question_count = Question.objects.count()
    my_param = Question.objects.filter(
    Q(exam__subject__name__icontains=name)
    ).select_related(
        "exam__subject"
    ).values(
        "id",
        "exam__subject__name",
        "question_text",
        "score",
    )
    return render(request, 'question_view.html', {'my_param': my_param,'subject_count':subject_count,'student_count':student_count,'question_count':question_count})

