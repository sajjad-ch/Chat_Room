from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(min_length=1 ,max_length=20)
    last_name = forms.CharField(min_length=1 ,max_length=20)
    username = forms.CharField(min_length=1 ,max_length=20)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password1')
        confirm_password = self.cleaned_data.get('password2')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('password and confirm password are not the same.')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='confirm_password',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('password and confirm password are not the same.')