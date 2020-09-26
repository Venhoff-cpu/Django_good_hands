from django.urls import path

from .views import LandingPage, LoginView, LogoutView, RegisterView, AddDonationView, AddDonationConfirmation, \
    GetInstitutions, DonationProcessingView, ProfileView, PickUpConfirmationView, ProfileSettingsView, ChangePasswordView

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('profile/settings/pass-change/', ChangePasswordView.as_view(), name='profile-pass-change'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('form/', AddDonationView.as_view(), name='form'),
    path('form/confirmation/', AddDonationConfirmation.as_view(), name='form-pass'),
    path('profile/pick-up-confirmation', PickUpConfirmationView.as_view(), name='picked-up'),
    path('ajax/form/', DonationProcessingView.as_view(), name='form-ajax'),
    path('ajax/categories/', GetInstitutions.as_view(), name='ajax-institutions'),
]
