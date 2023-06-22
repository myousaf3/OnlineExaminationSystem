from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import (
    render,
    redirect,
)
from exam.forms import (
    UserLoginForm,
)


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "User Logged-In")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "login.html", context)
