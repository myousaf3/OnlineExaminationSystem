from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.shortcuts import (
    render,
    redirect,
)
from exam.models import (
    Exam,
)


@login_required(login_url="login")
@permission_required("auth.view_user")
def approve_exam(request, exam_id):
    if request.method == "POST" and request.user.is_superuser:
        try:
            exam = Exam.objects.get(id=exam_id)
            exam.is_approved = True
            exam.is_requested = False
            exam.save()
            return redirect("exam_list")

        except Exam.DoesNotExist as e:
            context = {"error": str(e)}
            return render(request, "admin/error.html", context)

        except Exception as e:
            context = {"error": str(e)}
            return render(request, "admin/error.html", context)

    else:
        return render(request, "admin/access_denied.html")
