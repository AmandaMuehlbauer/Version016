from django.contrib import admin
from django.urls import path
from StripePayment.views import (
    CreateCheckoutSessionView,
    SuccessView,
    CancelView,
    ProductLandingPageView,
    stripe_webhook,
)

app_name = 'StripePayment'  # Namespace for the app's URLs


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('productlanding/<int:pk>/', ProductLandingPageView.as_view(), name='landing'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),


]