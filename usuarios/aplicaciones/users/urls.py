from django.urls import path
from . import views

app_name = "user_app"

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name="registerU"),
    path('login/', views.LoginUser.as_view(), name="loginUser"),
    path('logout/', views.LogoutUser.as_view(), name="logoutUser"),
    path('update/', views.UpdatePasswordView.as_view(), name="updateUser"),
    path('verification/<pk>/', views.CodeVericationView.as_view(), name="verificationUser"),
]