from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    get_object_or_404,
)

from exam.views.views import is_student
from exam.models import (
    Attempt,
    AttemptQuestion,
)


@login_required(login_url="login")
@user_passes_test(is_student)
def check_exam_view(request, exam_id):
    user = request.user

    try:
        attempt_score = get_object_or_404(Attempt, student=user, exam_id=exam_id)
    except Http404:
        raise PermissionDenied("You are not authorized to view this exam.")

    attempted_questions = AttemptQuestion.objects.filter(
        student=user, question__exam_id=exam_id
    )

    return render(
        request,
        "check-exam-view.html",
        {
            "exam_id": exam_id,
            "attempt_score": attempt_score,
            "attempted_questions": attempted_questions,
        },
    )
