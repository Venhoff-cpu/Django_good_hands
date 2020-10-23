from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Category, Donation, User, phone_regex, zip_code_regex


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={"placeholder": "Imię"}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={"placeholder": "Nazwisko"}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Adress e-mail"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}))

    def clean_username(self):
        if User.objects.filter(username=self.data["email"], is_active=True).exists():
            self.add_error("email", error="Email already in use")

        return self.data["email"]

    def clean(self):
        if self.data["password1"] != self.data["password2"]:
            self.add_error(None, error="Hasła muszą być identyczne.")
        return super().clean()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    login = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}))


class CustomResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.TextInput(attrs={"placeholder": "Email"}))


class ChangeUserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )
        widgets = {
            "email": forms.EmailInput(),
        }
        labels = {
            "first_name": "Imię",
            "last_name": "Naziwsko",
            "email": "Adress Email",
        }


# class CustomSetPasswordForm(forms.Form):
#     password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
#     password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat password")
#
#     def clean(self):
#         if self.data["password1"] != self.data["password2"]:
#             self.add_error(None, error="Passwords need to be identical")
#         return super().clean()


class CustomSetPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,
                                          'placeholder': 'Stare hasło'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Nowe hasło'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Powtórz nowe hasło'}),
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data["old_password"]
        if password1 and old_password:
            if password1 == old_password:
                raise ValidationError(
                    self.error_messages['identical_password'],
                    code='identical_password',
                )
        password_validation.validate_password(password1, self.user)
        return password1


class DonationForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    quantity = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={"step": "1"}))
    street = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Ulica nr. domum / nr. mieszkania"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Warszawa"}))
    phone_number = forms.CharField(
        validators=[phone_regex],
        widget=forms.TextInput(attrs={"placeholder": "666999666"}),
    )
    zip_code = forms.CharField(
        validators=[zip_code_regex],
        widget=forms.TextInput(attrs={"placeholder": "00-000"}),
    )
    pick_up_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(attrs={"placeholder": "dd/mm/yyyy"}),
    )
    pick_up_time = forms.TimeField(input_formats=["%H:%M"], widget=forms.TimeInput(attrs={"placeholder": "--:--"}))
    pick_up_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": "5"}))

    class Meta:
        model = Donation
        exclude = ("user", "is_taken", "is_taken_date")
