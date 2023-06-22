from django.views import View
from django.contrib import messages
from django.http import Http404
from django.utils.decorators import method_decorator
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
    QuestionForm,
    TextForm,
)
from exam.models import (
    Exam,
)


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(user_passes_test(is_teacher), name="dispatch")
class TextBasedView(View):
    template_name = "text-based.html"
    question_form_class = QuestionForm
    text_form_class = TextForm

    def get(self, request):
        question_form = self.question_form_class()
        text_form = self.text_form_class()
        return render(
            request,
            self.template_name,
            {
                "question_form": question_form,
                "text_form": text_form,
            },
        )

    def post(self, request):
        try:
            question_form = self.question_form_class(request.POST)
            text_form = self.text_form_class(request.POST)
            if question_form.is_valid() and text_form.is_valid():
                question = question_form.save(commit=False)
                question.question_type = "text_based"
                question.subject = question.exam.subject
                question.save()
                text = text_form.save(commit=False)
                text.question = question
                text.save()
                messages.success(request, "Question added")
                return redirect("text-based")
            if "request-btn" in request.POST:
                if Exam.objects.filter(is_requested=True).exists():
                    messages.warning(request, "Exam request already exists.")
                else:
                    exam_id = request.POST.get("exam_id")
                    exam = Exam.objects.get(id=exam_id)
                    exam.is_requested = True
                    exam.save()
        except Exam.DoesNotExist:
            raise Http404("Exam does not exist.")
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred. Please try again later.")
            return redirect("home")

        return render(
            request,
            "text-based.html",
            {
                "question_form": question_form,
                "text_form": text_form,
            },
        )
