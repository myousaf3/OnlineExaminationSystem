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
def cancel_exam(request, exam_id):
    try:
        if request.method == "POST" and request.user.is_superuser:
            exam = Exam.objects.get(id=exam_id)
            exam.is_requested = False
            exam.save()
            return redirect("exam_list")
        else:
            return render(request, "admin/access_denied.html")
    except Exam.DoesNotExist:
        return render(
            request, "admin/error.html", {"error": "The requested exam does not exist."}
        )
    except Exception as e:
        return render(request, "admin/error.html", {"error": str(e)})
