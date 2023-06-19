from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponse,
)
from .forms import (
    SignUpForm,
    UserLoginForm,
    ExamForm,
    QuestionForm,
    OptionForm,
    TextForm,
    GroupForm,
    ProfileForm,
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
from django.utils import timezone


def create_profile(request):
    # Check if the user already has a profile
    try:
        existing_profile = request.user.profile
    except Profile.DoesNotExist:
        existing_profile = None

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=existing_profile)
        if form.is_valid():
            # Save the updated or new profile object
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=existing_profile)
    return render(request, "create_profile.html", {"form": form})


def is_teacher(user):
    return user.groups.filter(name="Teacher").exists()


def is_student(user):
    return user.groups.filter(name="Student").exists()


def home(request):
    if request.user.is_authenticated:
        context = {}
    return render(request, "home.html", context)


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        form.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("create_profile")
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
                return redirect("home")
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
        exam = Exam.objects.filter(is_approved=True)
        attempts = Attempt.objects.filter(exam__in=exam)
        form = GroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            group = form.cleaned_data["group"]
            user = user  # Or get the desired user object
            send_mail(
                "Testing Mail",
                f"Your username: {user} has been registered in the for along with your Email ID: {user.email} as {group}",
                "yousaf.munawar@gmail.com",
                {user.email},
                fail_silently=False,
            )
            user.groups.add(group)
            return redirect("exam_list")
        else:
            form = GroupForm()
        return render(
            request,
            "admin/exam_list.html",
            {"form": form, "attempts": attempts, "exams": exams},
        )
    else:
        return render(request, "admin/access_denied.html")


@login_required(login_url="login")
def approve_exam(request, exam_id):
    if request.method == "POST" and request.user.is_superuser:
        exam = Exam.objects.get(id=exam_id)
        exam.is_approved = True
        exam.is_requested = False
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
@user_passes_test(is_teacher)
def exam_submission(request):
    subjects = Subject.objects.all()
    subject_count = Subject.objects.count()
    student_count = User.objects.count()
    question_count = Question.objects.count()
    exams = Exam.objects.annotate(question_count=Count("question"))
    questions = Question.objects.all()
    if "request-btn" in request.POST:
        if Exam.objects.filter(is_requested=True).exists():
            messages.warning(request, "Exam request already exists.")
        else:
            exam_id = request.POST.get("exam_id")
            exam = Exam.objects.get(id=exam_id)
            exam.is_requested = True
            exam.save()
    return render(
        request,
        "exam-submission.html",
        {
            "subjects": subjects,
            "subject_count": subject_count,
            "student_count": student_count,
            "question_count": question_count,
            "exams": exams,
            "questions": questions,
        },
    )


@login_required(login_url="login")
@user_passes_test(is_teacher)
def create_exam(request):
    if request.method == "POST":
        exam_form = ExamForm(request.POST)
        if exam_form.is_valid():
            exam = exam_form.save()
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
    return render(request, "create-exam.html", {"exam_form": exam_form})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    exam_pk = question.exam.pk  # get the pk of the related Exam instance
    question.delete()
    return redirect(
        "/exam-submission/", pk=exam_pk
    )  # redirect the user to the related Exam detail view


@login_required(login_url="login")
@user_passes_test(is_teacher)
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
        "question-view.html",
        {
            "my_param": my_param,
            "subject_count": subject_count,
            "student_count": student_count,
            "question_count": question_count,
        },
    )


@login_required(login_url="login")
@user_passes_test(is_student)
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
    now = timezone.now()
    upcoming_exams = Exam.objects.filter(start_time__gt=now)
    visible_exams = Exam.objects.filter(is_visible=True)
    return render(
        request,
        "student-dashboard.html",
        {
            "upcoming_exams": upcoming_exams,
            "visible_exams": visible_exams,
            "now": now,
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
def questions_take(request):
    return render(request, "questions-take.html")


@login_required(login_url="login")
@user_passes_test(is_student)
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
            opt_answer = Option.objects.filter(
                Q(text_answer__icontains=request.POST["answer"])
            )
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
@user_passes_test(is_student)
def check_exam_view(request, exam_id):
    user = request.user
    attempted_questions = AttemptQuestion.objects.filter(
        student=user, question__exam_id=exam_id
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


@login_required(login_url="login")
@user_passes_test(is_teacher)
def mcq_based(request):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        option_form = OptionForm(request.POST)
        if question_form.is_valid() and option_form.is_valid():
            question = question_form.save(commit=False)
            question.question_type = "multiple_choice"
            question.subject = question.exam.subject
            question.save()
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
        "mcq-based.html",
        {
            "question_form": question_form,
            "option_form": option_form,
        },
    )


@login_required(login_url="login")
@user_passes_test(is_teacher)
def text_based(request):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        text_form = TextForm(request.POST)
        if question_form.is_valid() and text_form.is_valid():
            question = question_form.save(commit=False)
            question.question_type = "text_based"
            question.subject = question.exam.subject
            question.save()
            text = text_form.save(commit=False)
            text.question = question
            text.save()
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
        text_form = TextForm()
    return render(
        request,
        "text-based.html",
        {
            "question_form": question_form,
            "text_form": text_form,
        },
    )
