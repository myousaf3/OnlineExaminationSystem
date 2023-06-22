from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import (
    render,
    redirect,
)
from exam.forms import (
    SignUpForm,
)


def signup(request):
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Form Submitted Success")
            return redirect("create_profile")
        else:
            error_message = form.errors.as_data().popitem()[1][0].message
            messages.error(request, error_message)
    context = {"form": form}
    return render(request, "signup.html", context)
