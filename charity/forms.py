from django import forms
from django.forms import ModelForm
from django.db import models

from .models import User, Donation, Institution, Category
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Adress e-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    login = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class DonationForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    quantity = forms.IntegerField(min_value=1,
                                  max_value=10,
                                  widget=forms.NumberInput(attrs={'step': '1'}))
    pick_up_date = forms.DateField(input_formats=['%d/%m/%Y'],
                                   widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    pick_up_time = forms.TimeField(input_formats=['%H:%M'],
                                   widget=forms.TimeInput(attrs={'placeholder': '--:--'}))
    pick_up_comment = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}))

    class Meta:
        model = Donation
        exclude = ('user', 'institution')
