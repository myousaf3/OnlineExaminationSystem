from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("exam-submission/", views.exam_submission, name="exam_submission"),
    path("question-view/<str:name>/", views.question_view, name="question"),
    path("question-view/<int:pk>", views.delete_question, name="question_delete"),
    path("question-view/take", views.questions_take, name="questions-take"),
    path("student-dashboard/", views.student_view, name="student_dashboard"),
    path("student/start-exam/", views.start_exam_view, name="start_exam_view"),
    path("student/<int:exam_id>/take/", views.start_exam_view, name="take_exam"),
    path("student/<int:exam_id>/check/", views.check_exam_view, name="check_exam"),
    path("accounts/login/", views.user_login, name="login"),
    path("exams/", views.exam_list, name="exam_list"),
    path("exams/create/", views.create_exam, name="create_exam"),
    path("exams/mcq-based", views.mcq_based, name="mcq-based"),
    path("exams/text-based", views.text_based, name="text-based"),
    path("exams/<int:exam_id>/cancel/", views.cancel_exam, name="cancel_exam"),
    path("exams/<int:exam_id>/approve/", views.approve_exam, name="approve_exam"),
    path('create-profile/', views.create_profile, name='create_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
