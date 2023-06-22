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
    OptionForm,
)
from exam.models import (
    Exam,
)


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(user_passes_test(is_teacher), name="dispatch")
class MCQBasedView(View):
    template_name = "mcq-based.html"
    question_form_class = QuestionForm
    option_form_class = OptionForm

    def get(self, request, *args, **kwargs):
        question_form = self.question_form_class()
        option_form = self.option_form_class()
        return render(
            request,
            self.template_name,
            {
                "question_form": question_form,
                "option_form": option_form,
            },
        )

    def post(self, request, *args, **kwargs):
        try:
            question_form = self.question_form_class(request.POST)
            option_form = self.option_form_class(request.POST)
            if question_form.is_valid() and option_form.is_valid():
                question = question_form.save(commit=False)
                question.question_type = "multiple_choice"
                question.subject = question.exam.subject
                question.save()
                option = option_form.save(commit=False)
                option.question = question
                option.save()
                messages.success(request, "Question added")
                return redirect("mcq-based")
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
            "mcq-based.html",
            {
                "question_form": question_form,
                "option_form": option_form,
            },
        )
