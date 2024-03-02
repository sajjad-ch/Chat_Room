from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('forgot_password', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset_password', views.ResetPasswordView.as_view(), name='reset_password_page'),
]
