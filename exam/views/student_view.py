from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
)

from exam.views.views import is_student
from exam.models import (
    Question,
    Subject,
    User,
    Exam,
    Attempt,
)


@login_required(login_url="login")
@user_passes_test(is_student)
def student_view(request):
    try:
        profile = request.user.profile
        attempts = Attempt.objects.filter(student=request.user)
        attempted_exams = [attempt.exam.id for attempt in attempts]
        exams = Exam.objects.exclude(id__in=attempted_exams)

        now = timezone.now()
        upcoming_exams = exams.filter(start_time__gt=now)

        visible_exams = []
        for exam in exams:
            if exam.is_approved and exam.start_time <= now <= exam.end_time:
                exam.is_visible = True
                visible_exams.append(exam)
            else:
                exam.is_visible = False

        subject_count = Subject.objects.count()
        student_count = User.objects.count()
        question_count = Question.objects.count()
        exam_count = exams.count()

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
                "exams": exams,
            },
        )
    except Exception as e:
        context = {"error": str(e)}
        return render(request, "admin/error.html", context)
