from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from chat.models import UserProfile
from django.http import HttpRequest
from django.contrib.auth import login, logout
from . import forms
# Create your views here.

class RegisterView(View):
    def get(self, request:HttpRequest):
        register_form = forms.RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request:HttpRequest):
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            user_firstname = register_form.cleaned_data.get('first_name')
            user_lastname = register_form.cleaned_data.get('last_name')
            user_username = register_form.cleaned_data.get('username')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password1')
            user: bool = User.objects.filter(email__iexact=user_email)
            if user:
                register_form.add_error('email', 'You already have an account. Please Log in.')
            else:
                new_user = User(
                    first_name=user_firstname,
                    last_name=user_lastname,
                    username=user_username,
                    email=user_email,
                )
                new_user.set_password(user_password)
                new_user.save()

                new_user_profile = UserProfile(name=user_firstname,
                                               email=user_email,
                                               username=user_username,
                                               user=new_user)
                new_user_profile.save()
                return redirect(reverse('login_page'))
        context = {
            'register_form': register_form
        }
        return render(request, 'accounts/register.html', context)


class LoginView(View):
    def get(self, request:HttpRequest):
        login_form = forms.LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request: HttpRequest):
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                is_password_correct = user.check_password(user_password)
                if is_password_correct:
                    login(request, user)
                    return redirect(reverse('home'))
                else:
                    login_form.add_error('email', 'password is incorrect!')
            else:
                login_form.add_error('email', 'Please Register first!')
        context = {
            'login_form': login_form
        }
        return render(request, 'accounts/login.html', context)

class ForgotPasswordView(View):
    def get(self, request: HttpRequest):
        forgot_password_form = forms.ForgotPasswordForm()
        context = {
            'forgot_password_form' : forgot_password_form
        }
        return render(request, 'accounts/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forgot_password_form = forms.ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user_email = forgot_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                return redirect(reverse('reset_password_page'))
            else:
                forgot_password_form.add_error('email', 'You do not have an account. Register first.')
        context = {
            'forgot_password_form': forgot_password_form
        }
        return render(request, 'accounts/forgot_password.html', context)

class ResetPasswordView(View):
    def get(self, request: HttpRequest):
        reset_password_form = forms.ResetPasswordForm()
        context = {
            'reset_password_form': reset_password_form
        }
        return render(request, 'accounts/reset_password.html', context)

    def post(self, request: HttpRequest):
        reset_password_form = forms.ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            user_email = reset_password_form.cleaned_data.get('email')
            user_new_password = reset_password_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is None:
                return redirect(reverse('login_page'))
            user.set_password(user_new_password)
            user.save()
            return redirect(reverse('login_page'))
        context = {
            'reset_password_form': reset_password_form
        }
        return render(request, 'accounts/reset_password.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))