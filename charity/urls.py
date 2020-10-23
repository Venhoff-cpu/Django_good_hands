from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import CustomResetPasswordForm
from .views import (
    AddDonationConfirmation,
    AddDonationView,
    ChangePasswordView,
    DonationDetailView,
    DonationProcessingView,
    GetInstitutions,
    LandingPage,
    LoginView,
    LogoutView,
    PickUpConfirmationView,
    ProfileSettingsView,
    ProfileView,
    RegisterView,
    VerificationView,
)

urlpatterns = [
    path("", LandingPage.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("register/confirmation/<user_id>/<token>/", VerificationView.as_view(), name="mail-activation"),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html",
        form_class=CustomResetPasswordForm),
         name='password_reset'),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/settings/", ProfileSettingsView.as_view(), name="profile-settings"),
    path(
        "profile/settings/pass-change/",
        ChangePasswordView.as_view(),
        name="profile-pass-change",
    ),
    path(
        "profile/donation/<int:pk>/",
        DonationDetailView.as_view(),
        name="donation-detail",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("form/", AddDonationView.as_view(), name="form"),
    path("form/confirmation/", AddDonationConfirmation.as_view(), name="form-pass"),
    path(
        "profile/pick-up-confirmation",
        PickUpConfirmationView.as_view(),
        name="picked-up",
    ),
    path("ajax/form/", DonationProcessingView.as_view(), name="form-ajax"),
    path("ajax/categories/", GetInstitutions.as_view(), name="ajax-institutions"),
]
