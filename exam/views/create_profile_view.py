from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (
    render,
    redirect,
)
from exam.forms import (
    ProfileForm,
)
from exam.models import (
    Profile,
)


class CreateProfileView(View):
    def get(self, request):
        try:
            existing_profile = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            existing_profile = None
        form = ProfileForm(instance=existing_profile)
        return render(request, "create_profile.html", {"form": form})

    def post(self, request):
        try:
            existing_profile = Profile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            existing_profile = None
        form = ProfileForm(request.POST, request.FILES, instance=existing_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile created successfully!")
            return redirect("home")
        else:
            return render(request, "create_profile.html", {"form": form})
