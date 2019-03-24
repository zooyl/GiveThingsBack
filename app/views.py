from django.shortcuts import render
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin


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
