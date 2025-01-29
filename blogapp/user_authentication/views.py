from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm

from apps.profiles.models import Profile

from utilities.authenticators import when_logged_outc, when_logged_in

# Create your views here.
class RegisterView(View):

    @when_logged_outc
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'register_form' : form
        }
        return render(request, 'register.html', context)

    @when_logged_outc
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            personal_profile = Profile(user = user)
            personal_profile.save()
            login(request, user)
            return redirect('/welcome')
        valid_username = form.cleaned_data['username'] != None and form.cleaned_data['username'] != 'myprofile'
        valid_email = 'email' in form.cleaned_data and not User.objects.filter(email=form.cleaned_data.get('email')).exists()
        valid_password = 'password_mismatch' not in form.error_messages

        form.validate_fields(valid_username, valid_email, valid_password)
        context = {
            'register_form' : form
        }
        return render(request, 'register.html', context)

class LoginView(View):

    @when_logged_outc
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'login_form' : form
        }
        return render(request, 'login.html', context)

    @when_logged_outc
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/welcome')

        form = LoginForm()
        form.validate_fields()
        context = {
            'login_form' : form
        }
        return render(request, 'login.html', context)
    
@when_logged_in
def LogoutView(request, *args, **kwargs):
    logout(request)
    return render(request, 'logout.html', {})