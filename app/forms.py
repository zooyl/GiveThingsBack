import django.forms as forms
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from app.models import Gathering
import re


class CustomUserCreationForm(forms.Form):
    email = forms.CharField(label='Email', validators=[EmailValidator()])
    password1 = forms.CharField(label='Haslo', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtorz haslo', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Hasla nie sa takie same')
        if len(p1) < 8:
            raise forms.ValidationError("Haslo musi zawierac przynajmniej 8 znakow")
        if not re.findall('[()[{}|`~!@#$%^&*,+=;:\'"<>./?]', p1):
            raise forms.ValidationError("Haslo musi zawierac znak specjalny")
        if not re.findall('[A-Z]', p1):
            raise forms.ValidationError("Haslo musi zawierac wielka litere")
        return cleaned_data

    def clean_email(self):
        data = self.cleaned_data['email']
        duplicate_users = User.objects.filter(email=data)
        if duplicate_users.exists():
            raise forms.ValidationError("Taki adres e-mail juz istnieje")
        return data


class GatheringForm1(forms.ModelForm):
    class Meta:
        model = Gathering
        fields = ['place', 'goal', 'needed']


class GatheringForm2(forms.ModelForm):
    class Meta:
        model = Gathering
        fields = ['time', 'description', 'photo']