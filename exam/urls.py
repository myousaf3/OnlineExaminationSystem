from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("exam-submission/", views.exam_submission, name="exam_submission"),
    path("question-view/<str:name>/", views.question_view, name="question"),
    path("question-view/<int:pk>", views.delete_question, name="question_delete"),
    path("student-dashboard/", views.student_view, name="student_dashboard"),
    path("student/take-exam/", views.take_exam_view, name="take_exam_view"),
    path("student/start-exam/", views.start_exam_view, name="start_exam_view"),
    path("student/<int:exam_id>/take/", views.start_exam_view, name="take_exam"),
    path("student/<int:exam_id>/check/", views.check_exam_view, name="check_exam"),
    path("student/calculate-marks", views.calculate_marks_view, name="calculate-marks"),
    path("exams/", views.exam_list, name="exam_list"),
    path("exams/<int:exam_id>/approve/", views.approve_exam, name="approve_exam"),
    path("exams/<int:exam_id>/cancel/", views.cancel_exam, name="cancel_exam"),
    path("exams/create/", views.create_exam, name="create_exam"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
