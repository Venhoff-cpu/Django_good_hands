from django.contrib import admin
from django.urls import path

from .views import LandingPage, LoginView, RegisterView, AddDonation, AddDonationConfiramtion

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('form/', AddDonation.as_view(), name='form'),
    path('form/confirmation/', AddDonationConfiramtion.as_view(), name='form-pass')
]
