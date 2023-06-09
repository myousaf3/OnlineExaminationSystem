from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth
from . import views 

urlpatterns = [ 
    path('signup/', views.signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('exam-submission/', views.exam_submission, name="exam_submission"), 
    path('question-view/<str:name>/', views.question_view, name='question'),
    path('question-view/<int:pk>', views.delete_question, name='question_delete'),
] 
