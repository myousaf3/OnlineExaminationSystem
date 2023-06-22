from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
)

from exam.views.views import is_teacher
from exam.models import (
    Question,
    Subject,
    User,
)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def question_view(request, name):
    try:
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
    except Exception as e:
        context = {"error": str(e)}
        return render(request, "admin/error.html", context)
