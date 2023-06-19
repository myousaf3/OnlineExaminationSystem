from django.contrib import admin
from .models import (
    TempSessionScore,
    Profile,
    Subject,
    Exam,
    Question,
    Attempt,
    ApprovalRequest,
    Option,
    AttemptQuestion,
)

# Register your models here.

admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Attempt)
admin.site.register(AttemptQuestion)
admin.site.register(ApprovalRequest)
admin.site.register(TempSessionScore)
admin.site.register(Option)
