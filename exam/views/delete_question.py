from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from exam.views.views import is_teacher
from exam.models import (
    Question,
)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def delete_question(request, pk):
    try:
        question = get_object_or_404(Question, pk=pk)
        exam_pk = question.exam.pk
        question.delete()
        messages.success(request, "Question deleted successfully!")
        return redirect("/exam-submission/", pk=exam_pk)
    except Exception as e:
        context = {"error": str(e)}
        return render(request, "admin/error.html", context)
