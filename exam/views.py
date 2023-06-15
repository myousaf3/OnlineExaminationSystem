from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    redirect,
    HttpResponseRedirect,
    get_object_or_404,
)
from .forms import (
    SignUpForm,
    UserLoginForm,
    ExamForm,
    QuestionForm,
    OptionForm,
)
from exam.models import (
    Question,
    Subject,
    User,
    Exam,
    Option,
    Attempt,
    AttemptQuestion,
    Profile,
    TempSessionScore,
)
from django.db.models import Q


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        form.save()
        return redirect("login")
    context = {"form": form}
    return render(request, "signup.html", context)


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("exam_submission")
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "base.html", {"profile": profile})


@login_required(login_url="login")
def exam_list(request):
    if request.user.is_superuser:
        exams = Exam.objects.filter(is_requested=True)
        return render(request, "admin/exam_list.html", {"exams": exams})
    else:
        return render(request, "admin/access_denied.html")


@login_required(login_url="login")
def approve_exam(request, exam_id):
    if request.method == "POST" and request.user.is_superuser:
        exam = Exam.objects.get(id=exam_id)
        exam.is_approved = True
        exam.save()
        return redirect("exam_list")
    else:
        return render(request, "admin/access_denied.html")


@login_required(login_url="login")
def cancel_exam(request, exam_id):
    if request.method == "POST" and request.user.is_superuser:
        exam = Exam.objects.get(id=exam_id)
        exam.is_requested = False
        exam.save()
        return redirect("exam_list")
    else:
        return render(request, "admin/access_denied.html")


@login_required(login_url="login")
def exam_submission(request):
    subjects = Subject.objects.all()
    subject_count = Subject.objects.count()
    student_count = User.objects.count()
    question_count = Question.objects.count()
    exams = Exam.objects.all()
    questions = Question.objects.all()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        option_form = OptionForm(request.POST)
        if question_form.is_valid() and option_form.is_valid():
            question = question_form.save()
            option = option_form.save(commit=False)
            option.question = question
            option.save()
        if "request-btn" in request.POST:
            if Exam.objects.filter(is_requested=True).exists():
                messages.warning(request, "Exam request already exists.")
            else:
                exam_id = request.POST.get("exam_id")
                exam = Exam.objects.get(id=exam_id)
                exam.is_requested = True
                exam.save()
    else:
        question_form = QuestionForm()
        option_form = OptionForm()
    return render(
        request,
        "exam_submission.html",
        {
            "question_form": question_form,
            "option_form": option_form,
            "subjects": subjects,
            "subject_count": subject_count,
            "student_count": student_count,
            "question_count": question_count,
            "exams": exams,
            "questions": questions,
        },
    )


@login_required(login_url="login")
def create_exam(request):
    if request.method == "POST":
        exam_form = ExamForm(request.POST)
        if exam_form.is_valid():
            exam = exam_form.save(commit=False)
            exam.teacher = request.user
            existing_exam = Exam.objects.filter(
                subject=exam.subject,
            ).first()

            if existing_exam:
                messages.warning(request, "Exam already exists.")
            else:
                exam.save()
                return redirect("/exams/create", pk=exam.pk)
    else:
        exam_form = ExamForm()
    return render(request, "create_exam.html", {"exam_form": exam_form})


@login_required(login_url="login")
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    exam_pk = question.exam.pk  # get the pk of the related Exam instance
    question.delete()
    return redirect(
        "/exam-submission/", pk=exam_pk
    )  # redirect the user to the related Exam detail view


@login_required(login_url="login")
def question_view(request, name):
    subject_count = Subject.objects.count()
    student_count = User.objects.count()
    question_count = Question.objects.count()
    my_param = (
        Question.objects.filter(Q(exam__subject__name__icontains=name))
        .select_related("exam__subject")
        .values(
            "id",
            "exam__subject__name",
            "question_text",
            "score",
        )
    )

    return render(
        request,
        "question_view.html",
        {
            "my_param": my_param,
            "subject_count": subject_count,
            "student_count": student_count,
            "question_count": question_count,
        },
    )


@login_required(login_url="login")
def student_view(request):
    profile = request.user.profile
    attempts = Attempt.objects.filter(student=request.user)
    attempted_exams = [attempt.exam.id for attempt in attempts]
    # Exclude the exams that have already been attempted by the logged-in user
    exam = Exam.objects.exclude(id__in=attempted_exams)
    subject_count = Subject.objects.count()
    student_count = User.objects.count()
    question_count = Question.objects.count()
    exam_count = Exam.objects.count()
    return render(
        request,
        "student_dashboard.html",
        {
            "profile": profile,
            "attempts": attempts,
            "exam_count": exam_count,
            "subject_count": subject_count,
            "student_count": student_count,
            "question_count": question_count,
            "exam": exam,
        },
    )


@login_required(login_url="login")
def take_exam_view(request):
    return render(request, "take-exam.html")


@login_required(login_url="login")
def start_exam_view(request, exam_id):
    profile = request.user.profile
    print(request.POST)
    x_id = exam_id
    exam_id = Exam.objects.get(id=exam_id)
    questions = Question.objects.filter(exam=exam_id)
    options = Option.objects.filter(question__in=questions).order_by("id")
    paginator = Paginator(questions, 1)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    total_pages = paginator.num_pages

    if request.method == "POST":
        next_page_number = int(request.GET.get("page", 1)) + 1
        question_id = request.POST.get("question_id")
        print("question_id", question_id)
        selected = request.POST.get("1")
        print("selected", selected)
        option = options.filter(question_id=question_id).first()
        print("option is", option)
        q_id = questions.filter(id=question_id).first()
        print("questionid", q_id)
        temp_score = TempSessionScore.objects.first()
        fexam = Exam.objects.get(id=x_id)
        print(fexam)
        text_answer = request.POST.get("answer")
        print("text_answer is", text_answer)
        score = option.question.score
        answer = str(option.answer)
        print("answer", answer)
        if text_answer is not None:
            opt_answer = Option.objects.filter(Q(text_answer__icontains=request.POST['answer']))
            if opt_answer.exists():
                print("i am here hehehe")
                temp_score.score += score
                temp_score.save()
                AttemptQuestion.objects.create(
                    student=request.user,
                    question=q_id,
                    selected_option=text_answer,
                    is_correct=True,
                )
                if "exam_button" in request.POST and request.method == "POST":
                    attempt_completed = request.POST.get("attempt_completed")
                    if attempt_completed:
                        Attempt.objects.create(
                            student=profile.user,
                            exam=fexam,
                            score=temp_score.score,
                            is_attempted=True,
                        )
                        temp_score.score = 0
                        temp_score.save()
                        print(temp_score.score)
                        return redirect("/student-dashboard/")
                return redirect(f"/student/{x_id}/take/?page={next_page_number}")
            else:
                print(False)
                AttemptQuestion.objects.create(
                    student=request.user,
                    question=q_id,
                    selected_option=text_answer,
                    is_correct=False,
                )
                if "exam_button" in request.POST and request.method == "POST":
                    attempt_completed = request.POST.get("attempt_completed")
                    if attempt_completed:
                        Attempt.objects.create(
                            student=profile.user,
                            exam=fexam,
                            score=temp_score.score,
                            is_attempted=True,
                        )
                        temp_score.score = 0
                        temp_score.save()
                        print(temp_score.score)
                        return redirect("/student-dashboard/")
                return redirect(f"/student/{x_id}/take/?page={next_page_number}")
        if selected == answer:
            print(True)
            print(score)
            temp_score.score += score
            temp_score.save()
            print(temp_score)
            AttemptQuestion.objects.create(
                student=request.user,
                question=q_id,
                selected_option=selected,
                is_correct=True,
            )
            if "exam_button" in request.POST and request.method == "POST":
                attempt_completed = request.POST.get("attempt_completed")
                if attempt_completed:
                    Attempt.objects.create(
                        student=profile.user,
                        exam=fexam,
                        score=temp_score.score,
                        is_attempted=True,
                    )
                    temp_score.score = 0
                    temp_score.save()
                    print(temp_score.score)
                    return redirect("/student-dashboard/")
            return redirect(f"/student/{x_id}/take/?page={next_page_number}")
        else:
            print(False)
            AttemptQuestion.objects.create(
                student=request.user,
                question=q_id,
                selected_option=selected,
                is_correct=False,
            )
            if "exam_button" in request.POST and request.method == "POST":
                attempt_completed = request.POST.get("attempt_completed")
                if attempt_completed:
                    Attempt.objects.create(
                        student=profile.user,
                        exam=fexam,
                        score=temp_score.score,
                        is_attempted=True,
                    )
                    temp_score.score = 0
                    temp_score.save()
                    print(temp_score.score)
                    return redirect("/student-dashboard/")
            return redirect(f"/student/{x_id}/take/?page={next_page_number}")

    return render(
        request,
        "start-exam.html",
        {
            "options": options,
            "questions": questions,
            "exam_id": exam_id,
            "total_pages": total_pages,
            "page_obj": page_obj,
        },
    )


@login_required(login_url="login")
def check_exam_view(request, exam_id):
    user = request.user
    attempted_questions = AttemptQuestion.objects.filter(
        student=user,
        question__exam_id=exam_id
    )
    attempt_score = get_object_or_404(Attempt, student=user, exam_id=exam_id)
    return render(
        request,
        "check-exam-view.html",
        {
            "exam_id": exam_id,
            "attempt_score": attempt_score,
            "attempted_questions": attempted_questions,
        },
    )


def take_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = Question.objects.filter(exam=exam)
    question_scores = Question.objects.filter(exam=exam).values_list("score", flat=True)
    print(questions)

    # write a score queryset here
    if request.method == "POST":
        # Create a new attempt for the logged in user and the current exam
        attempt = Attempt.objects.create(exam=exam, score=question_scores)

        # Loop through all questions in the exam
        for question in questions:
            # Get the selected option from the form data
            selected_option_id = request.POST.get(f"question-{question.id}")

            # Create a new AttemptQuestion instance for the current question and selected option
            attempt_question = AttemptQuestion.objects.create(
                student=request.user,
                attempt=attempt,
                question=question,
                selected_option=Option.objects.get(id=selected_option_id),
            )

        return redirect("/exam-submission", attempt_id=attempt.id)

    context = {
        "exam": exam,
        "questions": questions,
    }
    return render(request, "basic_exam.html", context)


def calculate_marks_view(request):
    return HttpResponseRedirect("student-dashboard")
