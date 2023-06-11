from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth
from . import views 

urlpatterns = [ 
    path('signup/', views.signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('exam-submission/', views.exam_submission, name="exam_submission"), 
    path('student-dashboard/', views.student_view, name="student_dashboard"), 
    path('question-view/<str:name>/', views.question_view, name='question'),
    path('question-view/<int:pk>', views.delete_question, name='question_delete'),
    
    path('student/take-exam/', views.take_exam_view, name='take_exam_view'),
    path('student/start-exam/', views.start_exam_view, name='start_exam_view'),
    path('student/calculate-marks', views.calculate_marks_view,name='calculate-marks'),

] 
