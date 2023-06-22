from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    redirect,
)

from exam.views.views import is_teacher
from exam.models import (
    Question,
    Subject,
    User,
    Exam,
    Attempt,
)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def exam_submission(request):
    try:
        subjects = Subject.objects.all()
        subject_count = len(subjects)
        student_count = User.objects.count()
        question_count = Question.objects.count()
        exams = Exam.objects.annotate(question_count=Count("question"))
        exam = Exam.objects.filter(is_approved=True)
        attempts = Attempt.objects.filter(exam__in=exam)
        questions = Question.objects.all()

        if "request-btn" in request.POST:
            if Exam.objects.filter(is_requested=True).exists():
                messages.warning(request, "Exam request already exists!")
                return redirect("exam_submission")
            else:
                exam_id = request.POST.get("exam_id")
                exam = Exam.objects.get(id=exam_id)
                exam.is_requested = True
                exam.save()
                messages.success(request, "Exam requested successfully!")
                return redirect("exam_submission")
        return render(
            request,
            "exam-submission.html",
            {
                "attempts": attempts,
                "subjects": subjects,
                "subject_count": subject_count,
                "student_count": student_count,
                "question_count": question_count,
                "exams": exams,
                "questions": questions,
            },
        )
    except Exception as e:
        context = {"error": str(e)}
        return render(request, "admin/error.html", context)
