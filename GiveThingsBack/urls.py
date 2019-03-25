"""GiveThingsBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import app.views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
                  path('', app.views.landing_page, name='landing-page'),
                  path('activate/<uidb64>/<token>', app.views.Activate.as_view(), name='activate'),
                  path('register/', app.views.SignUp.as_view(), name='register'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('home/', app.views.Home.as_view(), name='home'),
                  path('settings/<pk>', app.views.Settings.as_view(), name='settings'),
                  path('change/password', app.views.ChangePassword.as_view(), name='change-password'),
                  path('admin/', admin.site.urls),
                  path('password/reset/',
                       PasswordResetView.as_view(template_name='registration/password_reset_email.html'),
                       name='password_reset'),
                  path('password/reset/done',
                       PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
                       name='password_reset_done'),
                  path('password/reset/confirm/<uidb64>/<token>',
                       PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
                       name='password_reset_confirm'),
                  path('password/reset/complete',
                       PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
                       name='password_reset_complete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
