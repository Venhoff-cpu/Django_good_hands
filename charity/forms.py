from django import forms
from django.forms import ModelForm

from .models import User, Donation, Category, phone_regex, zip_code_regex
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
    street = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ulica nr. domum / nr. mieszkania'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Warszawa'}))
    phone_number = forms.CharField(validators=[phone_regex],
                                   widget=forms.TextInput(attrs={'placeholder': '666999666'}))
    zip_code = forms.CharField(validators=[zip_code_regex],
                               widget=forms.TextInput(attrs={'placeholder': '00-000'}))
    pick_up_date = forms.DateField(input_formats=['%d/%m/%Y'],
                                   widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    pick_up_time = forms.TimeField(input_formats=['%H:%M'],
                                   widget=forms.TimeInput(attrs={'placeholder': '--:--'}))
    pick_up_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '5'}))

    class Meta:
        model = Donation
        exclude = ('user', 'is_taken', 'is_taken_date')
