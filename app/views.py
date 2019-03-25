from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.

def landing_page(request):
    return render(request, "index.html")


class SignUp(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            hashed_pass = make_password(form.cleaned_data['password1'])
            User.objects.create(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                password=hashed_pass)
            success = "Konto zostalo stworzone"
            return render(request, 'register.html', {'form': form, 'success': success})
        return render(request, 'register.html', {'form': form})


class Home(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = 'home'

    def get(self, request):
        user = request.user
        return render(request, "form.html", {'user': user})


class Settings(LoginRequiredMixin, UpdateView):
    login_url = "login"
    model = User
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('home')


class ChangePassword(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "change_password.html", {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Odswieza sesje z nowym haslem - uzytkownik nie musi sie ponownie logowac
            update_session_auth_hash(request, form.user)
            return redirect('home')
        return render(request, "change_password.html", {'form': form})
