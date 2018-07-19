from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import ValidationError

def validateEmail(email):

    try:
        User.objects.get(email=email)

    except User.DoesNotExist:

        raise ValidationError(" Invaid user! ")

class ForgotPassword(forms.Form):

    email = forms.EmailField(validators=[validateEmail])
    password1 = forms.CharField(
        label='Password',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm-Password',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput
    )
    def clean(self):

        form_data = self.cleaned_data

        if 'username' in form_data:
            if form_data['username'].isdigit():
                self.errors['username'] = ['Employee name cannot be digits']

        if 'password1' in form_data and 'password2' in form_data:
            if form_data['password1'] != form_data['password2']:
                self.errors['password2'] = ['password mismatch']

        return form_data



class LoginForm(forms.Form):

    username = forms.CharField(max_length=20)
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput
    )

def checkEmail(value):
    print(dir(User))

    try:
        User.objects.get(email=value)
        raise ValidationError("Email Already Exits!")
    except User.DoesNotExist:
        pass

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',

        min_length=8,
        max_length=20,
        widget=forms.PasswordInput
    )

    email = forms.EmailField(validators=[checkEmail])


class SignUpform(forms.Form):

    username = forms.CharField(min_length=6, max_length=20)
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm-Password',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput
    )

    def clean(self):

        form_data = self.cleaned_data

        if 'username' in form_data:
            if form_data['username'].isdigit():
                self.errors['username'] = ['Employee name cannot be digits']

        if 'password1' in form_data and 'password2' in form_data:
            if form_data['password1'] != form_data['password2']:
                self.errors['password2'] = ['password mismatch']

        return form_data