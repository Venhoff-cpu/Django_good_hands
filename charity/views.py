from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.views.generic import DetailView, FormView, TemplateView, UpdateView, View
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import get_template
from django.urls import reverse

from .forms import (
    ChangeUserForm,
    CustomSetPasswordForm,
    DonationForm,
    LoginForm,
    RegisterForm,
)
from .models import Category, Donation, Institution, User
from .tokens import account_activation_token
import Good_hands.settings as settings


class LandingPage(TemplateView):
    """
    Displays landing page.
    """
    template_name = "charity/index.html"
    
    def setup(self, request, *args, **kwargs):
        self.fou_paginator = Paginator(Institution.objects.filter(type="FUN"), 5)
        self.ngos_paginator = Paginator(Institution.objects.filter(type="NGO"), 5)
        self.local_paginator = Paginator(Institution.objects.filter(type="LOC"), 5)

        super(LandingPage, self).setup(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        """
        Provides to context total number of donated bags, and number of actively supported institutions -
        institutions which received at least one donation.
        Provides all verified institutions split into types.
        """
        ctx = {}
        helped_organizations = Donation.objects.values("institution").distinct().count()
        num_of_bags = Donation.objects.all().aggregate(Sum("quantity"))

        model_fou = self.fou_paginator.page(1)
        model_ngo = self.ngos_paginator.page(1)
        model_local = self.local_paginator.page(1)

        ctx["organizations"] = helped_organizations
        ctx["bags"] = num_of_bags["quantity__sum"] or 0
        ctx["foundations"] = model_fou
        ctx["ngos"] = model_ngo
        ctx["local_collections"] = model_local
        return ctx
    
    def post(self, request):
        paginator_typ = self.request.POST.get('type_of_paginator')
        page_num = self.request.POST.get('page_num')
        print(page_num)
        if paginator_typ == 'foundation':
            model_fou = self.fou_paginator.page(page_num)
            return render(self.request, 'charity/foundation-pagination.html', {'foundations': model_fou})
        elif paginator_typ == 'ngos':
            model_ngo = self.ngos_paginator.page(page_num)
            return render(self.request, 'charity/ngos-pagination.html', {'ngos': model_ngo})
        elif paginator_typ == 'local':
            model_local = self.local_paginator.page(page_num)
            return render(self.request, 'charity/local-pagination.html', {'local_collections': model_local})
        else:
            return JsonResponse({'message': 'Unrecognized institution list.'}, status=500)


class AddDonationView(LoginRequiredMixin, FormView):
    """
    Displays donation form Pages. Only available to authenticated users.
    """

    login_url = reverse_lazy("login")
    template_name = "charity/form.html"
    form_class = DonationForm


class DonationProcessingView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data["categories"]
            institution = form.cleaned_data["institution"]
            for category in categories:
                if not institution.categories.filter(pk=category.id).exists():
                    messages.error(
                        self.request,
                        "Coś poszło nie tak, proszę wypełnić formularz ponownie",
                    )
                    return redirect("form")

            new_donation = Donation.objects.create(
                quantity=form.cleaned_data["quantity"],
                street=form.cleaned_data["street"],
                city=form.cleaned_data["city"],
                zip_code=form.cleaned_data["zip_code"],
                phone_number=form.cleaned_data["phone_number"],
                pick_up_date=form.cleaned_data["pick_up_date"],
                pick_up_time=form.cleaned_data["pick_up_time"],
                pick_up_comment=form.cleaned_data["pick_up_comment"],
                user=request.user,
                institution=institution,
            )
            new_donation.categories.set(categories)

            return JsonResponse({"url": "confirmation/"})
        else:
            print(form.errors)


class GetInstitutions(View):
    def post(self, request):
        categories = request.POST.getlist("categories[]")
        institutions_all = Institution.objects.all().select_related('categories')
        if categories:
            for category_id in categories:
                category_id = int(category_id)
                institutions_all = institutions_all.filter(categories=Category.objects.get(pk=category_id))

        return render(request, "charity/form-institutions.html", {"institutions": institutions_all})


class AddDonationConfirmation(TemplateView):
    template_name = "charity/form-confirmation.html"


class LoginView(FormView):
    """
    Displays login view page. Provieds custom form for custom User.
    """

    form_class = LoginForm
    template_name = "charity/login.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("login")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.info(
                self.request,
                f"Jesteś zlogowany jako {user.first_name} {user.last_name}",
            )
        else:
            messages.info(self.request, "Brak uzytkownika o podanym adresie email")
            return redirect(reverse_lazy("register"))
        return redirect(reverse_lazy("index"))


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Displays user profile.
    """
    template_name = "charity/profile.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        donations = Donation.objects.filter(user=self.request.user)

        ctx = {
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "email": self.request.user.email,
            "donations": donations,
        }
        return ctx


class PickUpConfirmationView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request):
        donation = get_object_or_404(Donation, pk=request.POST.get("is_taken"))
        if request.user.id == donation.user.id:
            donation.is_taken = True
            donation.is_taken_date = datetime.now().date()
            donation.save()
            messages.info(
                self.request,
                f"Potwierdzono odbiór darów z dnia {donation.pick_up_date}",
            )
        else:
            messages.info(self.request, "Nie udało się potwierdzić odbioru.")

        return redirect("profile")


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    """Displays form for updating data about user profile"""

    login_url = reverse_lazy("login")
    form_class = ChangeUserForm
    template_name = "charity/profile-change.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the error below.")
        return super().form_invalid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("login")
    form_class = CustomSetPasswordForm
    template_name = "charity/profile-change-pass.html"
    success_url = reverse_lazy("profile")

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Password changed successfully.")
        return super(ChangePasswordView, self).get_success_url()


class RegisterView(FormView):
    """
    Displays register view page. Provides custom form for custom User.
    """
    template_name = "charity/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        """
        After validation, sends an email with activation link
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = account_activation_token.make_token(user)
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        url = 'http://localhost:8000' + reverse('mail-activation',
                                                kwargs={'user_id': user_id, 'token': token})
        message = get_template('charity/email-confirmation.html').render({
            'confirm_url': url,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        mail = EmailMessage('Django Good Hands potwierdzenie mailowe', message, to=[user.email],
                            from_email=settings.EMAIL_HOST_USER)
        mail.content_subtype = 'html'
        mail.send()
        messages.info(self.request, f"Maile potwierdzający rejestrację został wysłany na {user.email}. "
                                    f"Proszę potwierdzić by zakończyć rejestrację. Sprawdź spam.")
        return redirect('login')


class VerificationView(View):
    """
    Activation token validation.
    """
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))

        user = get_object_or_404(User, pk=user_id)

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(self.request, f"Rejestracja udana. Mozna się zalogować.")

        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Zostałeś wylogowany")
        return redirect(reverse_lazy("index"))


class DonationDetailView(LoginRequiredMixin, DetailView):
    """
    Displays details about single donation.
    """

    model = Donation
    template_name = "charity/donation-detail.html"
    context_object_name = "donation"
    login_url = reverse_lazy("login")

    # def get_object(self, queryset=None):
    #     queryset = super(DonationDetailView, self).get_queryset()
    #     return queryset.filter(user=self.request.user)
