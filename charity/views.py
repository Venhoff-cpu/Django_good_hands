from django.core.paginator import Paginator
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
        all_institutions = Institution.objects.all()

        fou_paginator = Paginator(all_institutions.filter(type='FUN'), 5)
        ngos_paginator = Paginator(all_institutions.filter(type='NGO'), 5)
        local_paginator = Paginator(all_institutions.filter(type='LOC'), 5)

        page_fou = self.request.GET.get('page_fou')
        page_ngo = self.request.GET.get('page_ngo')
        page_local = self.request.GET.get('page_local')

        ctx['organizations'] = helped_organizations
        ctx['bags'] = num_of_bags['quantity__sum']
        ctx['foundations'] = fou_paginator
        ctx['ngos'] = ngos_paginator.get_page(page_ngo)
        ctx['local_collections'] = local_paginator.get_page(page_local)
        return ctx


class AddDonation(TemplateView):
    template_name = 'form.html'


class AddDonationConfiramtion(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
