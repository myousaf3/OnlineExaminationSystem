from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.shortcuts import (
    render,
    redirect,
)
from exam.forms import (
    GroupForm,
)
from exam.models import (
    Exam,
    Attempt,
)


@login_required(login_url="login")
@permission_required("auth.view_user")
def exam_list(request):
    if request.user.is_superuser:
        try:
            exams = Exam.objects.filter(is_requested=True)
            exam = Exam.objects.filter(is_approved=True)
            attempts = Attempt.objects.filter(exam__in=exam)

            if request.method == "POST":
                form = GroupForm(request.POST)
                if form.is_valid():
                    user = form.cleaned_data["user"]
                    group = form.cleaned_data["group"]
                    send_mail(
                        "Testing Mail",
                        f"Your username: {user} has been registered in the for along with your Email ID: {user.email} as {group}",
                        "yousaf.munawar@gmail.com",
                        [user.email],
                        fail_silently=False,
                    )
                    user.groups.add(group)
                    messages.success(request, "Role is defined to the user.")
                    return redirect("exam_list")

            else:
                form = GroupForm()

            context = {"form": form, "attempts": attempts, "exams": exams}
            return render(request, "admin/exam_list.html", context)

        except Exception as e:
            context = {"error": str(e)}
            return render(request, "admin/error.html", context)

    else:
        return render(request, "admin/access_denied.html")
