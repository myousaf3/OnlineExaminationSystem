from django.urls import path
from django.contrib.auth import views
from . import views 

urlpatterns = [ 
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login") 
] 
