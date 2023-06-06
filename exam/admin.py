from django.contrib import admin
from .models import Profile,Subject,Exam,Question,Attempt,ApprovalRequest,Option,Answer

# Register your models here.

admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Attempt)
admin.site.register(ApprovalRequest)
admin.site.register(Option)
admin.site.register(Answer)