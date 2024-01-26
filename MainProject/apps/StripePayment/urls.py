#apps/StripePayment/urls.py
from django.contrib import admin
from django.urls import path
from StripePayment.views import (
    DonationView,
    DonationSuccessView,
    DonationCancelView,
    SubscriptionView,
    SubscriptionSuccessView,
    SubscriptionCancelView,
    CreateSubscriptionCheckoutSessionView,
    CombinedView,
    


)

app_name = 'StripePayment'  # Namespace for the app's URLs


urlpatterns = [
    path('admin/', admin.site.urls),

    path('donation/', DonationView.as_view(), name='donation-view'),  # Map the DonationView to a URL

    path('donation-cancel/', DonationCancelView.as_view(), name='donation-cancel'),
    path('donation-success/', DonationSuccessView.as_view(), name='donation-success'),

    path('subscription/', SubscriptionView.as_view(), name='subscription-view'),
    path('create-subscription-session/', CreateSubscriptionCheckoutSessionView.as_view(), name='create-subscription-session'),
 
    path('subscription-success/', SubscriptionSuccessView.as_view(), name='subscription_success'),
    path('subscription-cancel/', SubscriptionCancelView.as_view(), name='subscription_cancel'),

    path('donate/',  CombinedView.as_view(), name='combined-donation'),
    path('unsubscribe/<int:subscription_id>/', SubscriptionView.as_view(), name='unsubscribe_subscription'),

 #   path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
  #  path('custom-payment/', CustomPaymentView.as_view(), name='custom-payment'),
  #  path('combined/', CombinedView.as_view(), name='combined_view'),


]