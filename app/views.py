from django.views import View
from .forms import CustomUserCreationForm
from .models import Category, Foundation, SiteUser, GiveAway
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db.models import Sum


# Create your views here.

def landing_page(request):
    # it sum entire column, display it as a list. So values [0] print only number
    bags = list(GiveAway.objects.aggregate(Sum('bags')).values())[0]
    foundation_count = GiveAway.objects.values('foundation_id').distinct().count()
    foundation = Foundation.objects.all()
    return render(request, "index.html", {'bags': bags, 'foundation_count': foundation_count,
                                          'foundation': foundation})


class SignUp(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            hashed_pass = make_password(form.cleaned_data['password1'])
            new = User.objects.create(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                      password=hashed_pass)
            # Set user to inactive and send him e-mail with activation link
            new.is_active = False
            new.save()

            current_site = get_current_site(request)
            subject = 'Uaktywnij konto'
            message = render_to_string('account_activation_email.html', {
                'user': new,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new.pk)).decode(),
                'token': account_activation_token.make_token(new),
            })
            new.email_user(subject, message)
            success = "Na podany adres e-mail wyslalismy link aktywacyjny"
            return render(request, "registration/invalid.html", {"success": success})
        return render(request, 'register.html', {'form': form})


class Activate(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            fail = "Link jest nieprawidlowy. Konto nie zostalo aktywowane"
            return render(request, 'registration/invalid.html', {'fail': fail})


class Home(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = 'home'

    def get(self, request):
        user = request.user
        return render(request, "form_oryg.html", {'user': user})


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
            # Refresh session with new password - user doesnt have to log in again
            update_session_auth_hash(request, form.user)
            return redirect('home')
        return render(request, "change_password.html", {'form': form})


class GiveawayForm1(View):

    def get(self, request):
        category = Category.objects.all()
        return render(request, 'form_1.html', {'category': category})

    def post(self, request):
        category = request.POST['category']
        request.session['category'] = category
        return redirect('form2')


class GiveawayForm2(View):

    def get(self, request):
        return render(request, 'form_2.html')

    def post(self, request):
        bags = request.POST['bags']
        request.session['bags'] = bags
        return redirect('form3')


class GiveawayForm3(View):

    def get(self, request):
        foundation = Foundation.objects.all()
        return render(request, 'form_3.html', {'foundation': foundation})

    def post(self, request):
        foundation = request.POST['foundation']
        request.session['foundation'] = foundation
        return redirect('form4')


class GiveawayForm4(View):

    def get(self, request):
        return render(request, 'form_4.html')

    def post(self, request):
        street = request.POST['street']
        city = request.POST['city']
        postal = request.POST['postal']
        phone = request.POST['phone']
        date = request.POST['date']
        time = request.POST['time']
        details = request.POST['details']
        request.session['street'] = street
        request.session['city'] = city
        request.session['postal'] = postal
        request.session['phone'] = phone
        request.session['date'] = date
        request.session['time'] = time
        request.session['details'] = details
        return redirect('form5')


class GiveawayForm5(View):

    def get(self, request):
        category = request.session.get('category')
        bags = request.session.get('bags')
        foundation = request.session.get('foundation')
        street = request.session.get('street')
        city = request.session.get('city')
        postal = request.session.get('postal')
        phone = request.session.get('phone')
        date = request.session.get('date')
        time = request.session.get('time')
        details = request.session.get('details')
        return render(request, 'form_5.html', {
            'category': category,
            'bags': bags,
            'foundation': foundation,
            'street': street,
            'city': city,
            'postal': postal,
            'phone': phone,
            'date': date,
            'time': time,
            'details': details
        })

    def post(self, request):
        user = request.user
        category = Category.objects.get(name=request.session.get('category'))
        foundation = Foundation.objects.get(name=request.session.get('foundation'))
        new_giveaway = GiveAway.objects.create(category=category,
                                               bags=request.session.get('bags'),
                                               foundation=foundation)
        new_giveaway.count += 1
        new_giveaway.save()
        SiteUser.objects.create(user=user, donation=new_giveaway, street=request.session.get('street'),
                                city=request.session.get('city'), postal=request.session.get('postal'),
                                phone=request.session.get('phone'), date=request.session.get('date'),
                                details=request.session.get('details'))
        del request.session['category']
        del request.session['bags']
        del request.session['foundation']
        del request.session['street']
        del request.session['city']
        del request.session['postal']
        del request.session['phone']
        del request.session['date']
        del request.session['time']
        del request.session['details']
        return redirect('form6')


class GiveawayForm6(View):

    def get(self, request):
        return render(request, 'form_6.html')
