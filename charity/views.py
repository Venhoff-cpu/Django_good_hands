from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .models import Institution, Donation
from .forms import RegisterForm, LoginForm


class LandingPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = {}
        helped_organizations = Donation.objects.values('institution').distinct().count()
        num_of_bags = Donation.objects.all().aggregate(Sum('quantity'))
        all_institutions = Institution.objects.all()

        # fou_paginator = Paginator(all_institutions.filter(type='FUN'), 5)
        # ngos_paginator = Paginator(all_institutions.filter(type='NGO'), 5)
        # local_paginator = Paginator(all_institutions.filter(type='LOC'), 5)
        #
        # page_fou = self.request.GET.get('page_fou')
        # page_ngo = self.request.GET.get('page_ngo')
        # page_local = self.request.GET.get('page_local')

        ctx['organizations'] = helped_organizations
        ctx['bags'] = num_of_bags['quantity__sum']
        ctx['foundations'] = all_institutions.filter(type='FUN')
        ctx['ngos'] = all_institutions.filter(type='NGO')
        ctx['local_collections'] = all_institutions.filter(type='LOC')
        return ctx


class AddDonation(TemplateView):
    template_name = 'form.html'


class AddDonationConfiramtion(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        email = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email,
                            password=password)
        if user is not None:
            login(self.request, user)
            messages.info(self.request, f"Jesteś zlogowany jako {user.first_name} {user.last_name}")
        else:
            messages.info(self.request, f"Brak uzytkownika o podanym adresie email")
            return redirect(reverse_lazy('register'))
        return redirect(reverse_lazy('index'))


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class logout()