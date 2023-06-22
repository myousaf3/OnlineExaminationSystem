from django.urls import path
from . import views
from exam.views.start_exam_view import StartExamView
from exam.views.text_based_view import TextBasedView
from exam.views.create_profile_view import CreateProfileView
from exam.views.mcq_based_view import MCQBasedView
from exam.views.approve_exam import approve_exam
from exam.views.cancel_exam import cancel_exam
from exam.views.check_exam_view import check_exam_view
from exam.views.create_exam import create_exam
from exam.views.delete_question import delete_question
from exam.views.exam_list import exam_list
from exam.views.exam_submission import exam_submission
from exam.views.question_view import question_view
from exam.views.signup import signup
from exam.views.student_view import student_view
from exam.views.user_login import user_login
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500


urlpatterns = [
    path("", views.views.home, name="home"),
    path("logout/", views.views.user_logout, name="logout"),
    path("question-view/take", views.views.questions_take, name="questions-take"),
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("exam-submission/", exam_submission, name="exam_submission"),
    path("question-view/<str:name>/", question_view, name="question"),
    path("question-view/<int:pk>", delete_question, name="question_delete"),
    path("student-dashboard/", student_view, name="student_dashboard"),
    path("student/<int:exam_id>/check/", check_exam_view, name="check_exam"),
    path("accounts/login/", user_login, name="login"),
    path("exams/", exam_list, name="exam_list"),
    path("exams/create/", create_exam, name="create_exam"),
    path("exams/mcq-based", MCQBasedView.as_view(), name="mcq-based"),
    path("exams/text-based", TextBasedView.as_view(), name="text-based"),
    path("exams/<int:exam_id>/cancel/", cancel_exam, name="cancel_exam"),
    path("exams/<int:exam_id>/approve/", approve_exam, name="approve_exam"),
    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),
    path("start-exam/<int:exam_id>/", StartExamView.as_view(), name="start_exam"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
