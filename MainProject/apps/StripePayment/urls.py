#apps/StripePayment/urls.py
from django.contrib import admin
from django.urls import path
from StripePayment.views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    ProductLandingPageView,
    stripe_webhook,
    DonationView,
    DonationSuccessView,
    DonationCancelView,
    


)

app_name = 'StripePayment'  # Namespace for the app's URLs


urlpatterns = [
    path('admin/', admin.site.urls),

    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('productlanding/<int:pk>/', ProductLandingPageView.as_view(), name='productlanding'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

    path('donate/', DonationView.as_view(), name='donate'),  # Map the DonationView to a URL

    path('donation-cancel/', DonationCancelView.as_view(), name='donation-cancel'),
    path('donation-success/', DonationSuccessView.as_view(), name='donation-success'),
 #   path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
  #  path('custom-payment/', CustomPaymentView.as_view(), name='custom-payment'),


]