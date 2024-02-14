# legal/urls.py
from django.urls import path
from .views import privacy_policy, terms_of_service

urlpatterns = [
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
]
