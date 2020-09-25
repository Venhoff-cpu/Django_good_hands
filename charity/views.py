from datetime import datetime, date

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View, DetailView
from django.utils import timezone

from .models import Institution, Donation, Category, User
from .forms import RegisterForm, LoginForm, DonationForm


class LandingPage(TemplateView):
    """
    Displays landing page.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        Provides to context total number of donated bags, and number of actively supported institutions -
        institutions which received at least one donation.
        Provides all verified institutions split into types.
        """
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
        ctx['bags'] = num_of_bags['quantity__sum'] or 0
        ctx['foundations'] = all_institutions.filter(type='FUN')
        ctx['ngos'] = all_institutions.filter(type='NGO')
        ctx['local_collections'] = all_institutions.filter(type='LOC')
        return ctx


class AddDonationView(LoginRequiredMixin, FormView):
    """
    Displays donation form Pages. Only available to authenticated users.
    """
    login_url = reverse_lazy("login")
    template_name = 'form.html'
    form_class = DonationForm


class DonationProcessingView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            institution = form.cleaned_data['institution']
            for category in categories:
                if not institution.categories.filter(pk=category.id).exists():
                    messages.error(self.request, "Coś poszło nie tak, proszę wypełnić formularz ponownie")
                    return redirect('form')

            new_donation = Donation.objects.create(
                quantity=form.cleaned_data['quantity'],
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                zip_code=form.cleaned_data['zip_code'],
                phone_number=form.cleaned_data['phone_number'],
                pick_up_date=form.cleaned_data['pick_up_date'],
                pick_up_time=form.cleaned_data['pick_up_time'],
                pick_up_comment=form.cleaned_data['pick_up_comment'],
                user=request.user,
                institution=institution,
            )
            new_donation.categories.set(categories)

            return JsonResponse({'url': 'confirmation/'})
        else:
            print(form.errors)


class GetInstitutions(View):
    def post(self, request):
        categories = request.POST.getlist('categories[]')
        institutions_all = Institution.objects.all()
        if categories:
            for category_id in categories:
                category_id = int(category_id)
                institutions_all = institutions_all.filter(categories=Category.objects.get(pk=category_id))

        return render(request, 'form-institutions.html', {'institutions': institutions_all})


class AddDonationConfirmation(TemplateView):
    template_name = 'form-confirmation.html'


class LoginView(FormView):
    """
    Displays login view page. Provieds custom form for custom User.
    """
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


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Displays user profile.
    """
    template_name = 'profile.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        donations = Donation.objects.filter(user=self.request.user)

        ctx = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'donations': donations,
        }
        return ctx


class PickUpConfirmationView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request):
        donation = get_object_or_404(Donation, pk=request.POST.get('is_taken'))
        if request.user.id == donation.user.id:
            donation.is_taken = True
            donation.is_taken_date = datetime.now().date()
            donation.save()
            messages.info(self.request, f"Potwierdzono odbiór darów z dnia {donation.pick_up_date}")
        else:
            messages.info(self.request, "Nie udało się powteirdzić odbioru.")

        return redirect('profile')


class RegisterView(FormView):
    """
    Displays register view page. Provides custom form for custom User.
    """
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.info(request, "Zostałeś wylogowany")
        return redirect(reverse_lazy("index"))
