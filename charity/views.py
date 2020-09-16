from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Institution, Donation


class LandingPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = {}
        helped_organizations = Donation.objects.values('institution').distinct().count()
        num_of_bags = Donation.objects.all().aggregate(Sum('quantity'))
        ctx['organizations'] = helped_organizations
        ctx['bags'] = num_of_bags['quantity__sum']
        return ctx


class AddDonation(TemplateView):
    template_name = 'form.html'


class AddDonationConfiramtion(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
