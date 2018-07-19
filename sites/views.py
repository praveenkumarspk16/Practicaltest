from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from sites.forms import LoginForm, RegistrationForm,SignUpform, ForgotPassword
from django.contrib.auth.decorators import login_required


def staticExample(request):
    return render(request, 'site/static_example.html')


def ForgotPassword(request):
    form = ForgotPassword()
    message = ''
    if request.method == 'POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            message = 'Password reset done sucessfully!'
    return render(
        request,
        'site/forgot.html',
        {'form': form, 'msg': message})


def userLogin(request):
    if request.user.username:
        return redirect(userDashBoard)
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username,
                password=password
            )
            if user is None:
                message = 'User not found!'
            else:
                login(request, user)
                request.session['city'] = 'Bangalore'
                request.session['phone'] = '123456'
                return redirect(userDashBoard)
    return render(
        request,
        'site/login.html', {
            'form': form, 'msg': message
        }
    )


def userDashBoard(request):
    return render(request, 'site/dashboard.html')


def userLogout(request):
    logout(request)
    return redirect(userLogin)


def userRegistration(request):
    # if request.user.username:
    #   return redirect(userLogin)
    form = SignUpform()  # we can use Registerform also in signupform
    message = ''
    if request.method == 'POST':
        form = SignUpform(request.POST)
        if form.is_valid():
            user = User()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user.username = username
            user.email = form.cleaned_data['email']
            user.set_password(password)  # password has key
            # user,password = password   #raw password
            user.save()
            message = 'Registration done Successfully'

    return render(
        request,
        'site/registration.html',
        {'form': form, 'msg': message}
    )
