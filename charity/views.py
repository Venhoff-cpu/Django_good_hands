from django.shortcuts import render
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    template_name = 'index.html'


class AddDonation(TemplateView):
    template_name = 'form.html'


class AddDonationConfiramtion(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
