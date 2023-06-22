from django.views import View
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    redirect,
)

from exam.views.views import is_student
from exam.models import (
    Question,
    Exam,
    Option,
    Attempt,
    AttemptQuestion,
    TempSessionScore,
)


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(user_passes_test(is_student), name="dispatch")
class StartExamView(View):
    template_name = "start-exam.html"
    questions_per_page = 1

    def get(self, request, exam_id):
        profile = request.user.profile
        x_id = exam_id
        exam = Exam.objects.get(id=exam_id)
        questions = Question.objects.filter(exam=exam)
        options = Option.objects.filter(question__in=questions).order_by("id")
        paginator = Paginator(questions, self.questions_per_page)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        total_pages = paginator.num_pages

        context = {
            "options": options,
            "questions": questions,
            "exam_id": exam,
            "total_pages": total_pages,
            "page_obj": page_obj,
        }

        return render(request, self.template_name, context)

    def post(self, request, exam_id):
        profile = request.user.profile
        x_id = exam_id
        exam = Exam.objects.get(id=exam_id)
        questions = Question.objects.filter(exam=exam)
        options = Option.objects.filter(question__in=questions).order_by("id")
        paginator = Paginator(questions, self.questions_per_page)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        total_pages = paginator.num_pages

        next_page_number = int(request.GET.get("page", 1)) + 1
        question_id = request.POST.get("question_id")
        selected = request.POST.get("1")
        option = options.filter(question_id=question_id).first()
        q_id = questions.filter(id=question_id).first()
        temp_score = TempSessionScore.objects.first()
        fexam = Exam.objects.get(id=x_id)
        text_answer = request.POST.get("answer")
        score = option.question.score
        answer = str(option.answer)
        is_correct = False

        if text_answer is not None:
            opt_answer = Option.objects.filter(
                Q(text_answer__icontains=request.POST["answer"])
            )
            is_correct = opt_answer.exists()

        if selected == answer:
            is_correct = True

        temp_score.score += score if is_correct else 0
        temp_score.save()

        AttemptQuestion.objects.create(
            student=request.user,
            question=q_id,
            selected_option=text_answer if text_answer else selected,
            is_correct=is_correct,
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

        return redirect(f"/start-exam/{x_id}/?page={next_page_number}")
