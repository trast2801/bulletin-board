from django import forms
from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'author', 'id']
        labels = {
            'title': 'Название',
            'content': 'Содержание',
            'author': 'Автор',
            'id' : 'номер наверно автора'
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)
        labels = {
            'username' : 'Имя',
            'password1': 'пароль',
            'password2': 'пароль'
        }

class Tst(forms.Form):
    name = forms.CharField()

