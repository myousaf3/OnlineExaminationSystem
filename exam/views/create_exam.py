from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    redirect,
)

from exam.views.views import is_teacher
from exam.forms import (
    ExamForm,
)
from exam.models import (
    Exam,
)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def create_exam(request):
    try:
        if request.method == "POST":
            exam_form = ExamForm(request.POST)

            if exam_form.is_valid():
                exam = exam_form.save(commit=False)
                exam.teacher = request.user
                existing_exam = Exam.objects.filter(subject=exam.subject).first()

                if existing_exam:
                    messages.warning(request, "Exam already exists.")
                else:
                    exam.save()
                    messages.success(
                        request, "Exam Created! Now add questions to the exam."
                    )
                    return redirect("questions-take")
        else:
            exam_form = ExamForm()

        return render(request, "create-exam.html", {"exam_form": exam_form})
    except Exception as e:
        context = {"error": str(e)}
        return render(request, "admin/error.html", context)
