from django.contrib.auth import logout
from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from exam.models import (
    Profile,
)


def error_404(request, exception):
    return render(request, "404-page.html")


def error_500(request):
    return render(request, "500-page.html")


def is_teacher(user):
    return user.groups.filter(name="Teacher").exists()


def is_student(user):
    return user.groups.filter(name="Student").exists()


def home(request):
    return render(request, "home.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "base.html", {"profile": profile})


@login_required(login_url="login")
def questions_take(request):
    return render(request, "questions-take.html")
