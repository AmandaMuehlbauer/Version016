#apps/StripePayment/views.py
import stripe
from .models import Price, Product, Donation, Subscription
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.users.models import User
from stripe.error import StripeError
from StripePayment.utils import get_or_create_stripe_customer_id, create_stripe_checkout_session
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import logging
import json

 
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


class DonationView(View):
    template_name = "StripePayment/donation.html"

    def get(self, request, *args, **kwargs):
        # Logic to render the donation form
        return render(request, self.template_name, context={})

    def post(self, request, *args, **kwargs):
        # Logic to process the donation payment
        try:
            amount = int(request.POST.get('amount'))  # Assuming a form field for donation amount
            domain = "https://thewildernet.com"  # Default to thewildernet.com

            # Redirect www version to non-www if accessing through www
            if 'www.' in request.META.get('HTTP_HOST'):
                return redirect("https://thewildernet.com" + request.get_full_path(), permanent=True)

            # Adjust domain if in debug mode
            if settings.DEBUG:
                domain = "http://127.0.0.1:8000"  # Replace with your debug domain
                
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': amount * 100,  # Stripe uses amount in cents
                            'product_data': {
                                'name': 'Donation',  # Change as needed
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=domain + '/donation-success/',
                cancel_url=domain + '/donation-cancel/',
            )

            # Check if the user is authenticated before associating with the donation
            user = request.user if request.user.is_authenticated else None
                 
                # Create and save a Donation instance
            donation = Donation(
                amount=amount,
                stripe_checkout_session_id=checkout_session.id,
                user=user,  # Add the logged-in user to the donation
             #   stripe_customer_id=user.stripe_customer_id if user else None,

            )
            donation.save()

            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            # Handle the exception appropriately (e.g., show an error message)
            return render(request, self.template_name, context={'error_message': str(e)})

    def get_donation_info(self):
        return {}  



class DonationSuccessView(TemplateView):
    template_name = "StripePayment/donation_success.html"
 
class DonationCancelView(TemplateView):
    template_name = "StripePayment/donation_cancel.html"


#This view handles the subscriptions
class SubscriptionView(View):
    template_name = "StripePayment/subscription.html"

    def get_subscription_info(self, request, *args, **kwargs):
        try:
            subscription_info = []

            prices = stripe.Price.list(active=True, limit=10).data  # Retrieve subscription prices

            for price in prices:
                if price.type == 'recurring':
                    product = stripe.Product.retrieve(price.product)
 
                    if hasattr(product, 'name'):
                        price_amount = float(price.unit_amount_decimal) / 100  # Convert to integer and then divide by 100

                        subscription_info.append({
                            'id': price.id,  # Include the price ID
                            'product_name': product.name,
                            'price': "{:.2f}".format(price_amount),
                            'is_active': False,
                        })

            return subscription_info

        except stripe.error.StripeError as e:
        # Handle Stripe API errors
            messages.error(request, f'Stripe Error: {str(e)}')
            return []    

    def get_user_subscription_name(self, user):
    # Replace this with your logic to get the name of the user's subscription
        user_subscription = Subscription.objects.filter(user=user, is_active=True).first()
        return user_subscription.product if user_subscription else None

    def is_user_subscribed(self, user):
    # Replace this with your logic to check if the user is subscribed
        return Subscription.objects.filter(user=user, is_active=True).exists()


    def create_new_subscription(self, request):
        # Create a new instance of Subscription here
        return Subscription.objects.create(
            user=request.user,
            subscription_plan_id='default_plan',  # Set the default plan ID or use logic to determine it
            status='pending'
        )


    def get(self, request, *args, **kwargs):
       
        existing_stripe_customer_id = get_or_create_stripe_customer_id(request.user, create=True)
        subscription_info = self.get_subscription_info(request)
        user_subscribed = self.is_user_subscribed(request.user)
        user_subscription_name = self.get_user_subscription_name(request.user)


        context = {
            'subscription_info': subscription_info,
            'user_subscribed': user_subscribed,
            'user_subscription_name': user_subscription_name,
            'stripe_customer_id': existing_stripe_customer_id,
        }
        print(context)
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Set the Stripe secret key

        try:
            plan_id = request.POST.get('plan_id')  # Assuming a form field for subscription plan selection
            existing_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

            if existing_subscription:
            # User already has an active subscription, handle accordingly
                messages.warning(request, 'You are already subscribed to a plan.')
                return redirect('subscription_list')  # Change to your actual subscription list URL

        # Call the handle_subscription_selection method
            return self.handle_subscription_selection(request, plan_id)

        except stripe.error.StripeError as e:
        # Handle Stripe errors
            return render(request, self.template_name, {'error': str(e)})
        except ValueError as e:
        # Handle invalid plan ID error
            return render(request, self.template_name, {'error': str(e)})




class CreateSubscriptionCheckoutSessionView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get('plan_id')  # Assuming the plan_id is sent from the form
        user = request.user
        existing_subscription = Subscription.objects.filter(user=user, is_active=True).first()

        if existing_subscription:
            # If the user already has an active subscription, check if they are changing the plan
            if existing_subscription.subscription_plan_id == plan_id:
                messages.warning(request, 'You are already subscribed to this plan.')
                return redirect('subscription_list')
            else:
                # Cancel the existing subscription
                self.unsubscribe(request, existing_subscription.id)

        domain = "https://thewildernet.com"  # Default to thewildernet.com

        # Redirect www version to non-www if accessing through www
        if 'www.' in request.META.get('HTTP_HOST'):
            return redirect("https://thewildernet.com" + request.get_full_path(), permanent=True)

        # Adjust domain if in debug mode
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"  # Replace with your debug domain

        price = stripe.Price.retrieve(plan_id)
      #  subscription_amount = float(price.unit_amount_decimal) / 100  # Convert to integer and then divide by 100

        product = stripe.Product.retrieve(price.product)
       # product_name = product.name if hasattr(product, 'name') else "Unknown Product"


        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': plan_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=domain + '/subscription-success/',
            cancel_url=domain + '/subscription-cancel/',
        )


        return redirect(checkout_session.url)
    
    def unsubscribe(self, request, subscription_id):
        # Implement your logic to cancel the subscription
        pass

class SubscriptionSuccessView(TemplateView):
    template_name = "StripePayment/subscription_success.html"
 
class SubscriptionCancelView(TemplateView):
    template_name = "StripePayment/subscription_cancel.html"

class CombinedView(View):
    template_name = "StripePayment/donate.html"

    def fetch_donation_info(self):
        donation_view = DonationView()
        return donation_view.get_donation_info()

    def fetch_subscription_info(self, request):
        subscription_view = SubscriptionView()
        subscription_info = subscription_view.get_subscription_info(request)

        for subscription in subscription_info:
            price_id = subscription.get('id')
            if price_id:
                price = stripe.Price.retrieve(price_id)
                product = stripe.Product.retrieve(price.product)
                subscription['product_name'] = product.name if hasattr(product, 'name') else None
                subscription['price'] = float(price.unit_amount_decimal) / 100  # Convert from cents to dollars
        return subscription_info

    def get(self, request, *args, **kwargs):
        donation_info = self.fetch_donation_info()
        subscription_info = self.fetch_subscription_info(request)
        user_subscribed = self.user_subscribed(request.user)

        user_subscription_product = None
        user_subscription_price = 0.0

        if user_subscribed:
            user_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
            user_subscription_product = getattr(user_subscription, 'product', None)
            user_subscription_price = getattr(user_subscription, 'amount', 0.0)

        context = {
            'donation_info': donation_info,
            'subscription_info': subscription_info,
            'user_subscribed': user_subscribed,
            'user_subscription': {
                'product_name': user_subscription_product,
                'price': "{:.2f}".format(user_subscription_price),
            },
        }

        return render(request, self.template_name, context)

    def user_subscribed(self, user):
        if user.is_authenticated:
            return bool(Subscription.objects.filter(user=user, is_active=True).first())
        return False
    

#View for user to check their subscription
class SubscriptionListView(View):
    template_name = "StripePayment/subscription_list.html"

    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(user=request.user, is_active=True)
        context = {'subscriptions': subscriptions}
        return render(request, self.template_name, context)






def error_view(request, error_message="An unexpected error occurred."):
    return render(request, 'error.html', {'error_message': error_message})




def handle_checkout_session_completed(session):
    # Handle logic when a Checkout Session is completed
    subscription_id = session['line_items'][0]['price']['id']
    subscription = Subscription.objects.get(subscription_plan_id=subscription_id)
    
    # Update your model fields as needed
    subscription.is_active = True
    subscription.completed = 'yes'
    subscription.checkout_status = 'completed'

    # Save the changes
    subscription.save()

def handle_invoice_payment_succeeded(invoice):
    # Handle logic when an invoice payment is succeeded
    subscription_id = invoice['lines']['data'][0]['price']['id']
    subscription = Subscription.objects.get(subscription_plan_id=subscription_id)
    
    # Update your model fields as needed
    subscription.is_active = True
    subscription.completed = 'yes'
    subscription.checkout_status = 'completed'

    # Save the changes
    subscription.save()



@csrf_exempt
@require_POST

def webhook_subscription(request):
    payload = request.body
    sig_header = request.headers['Stripe-Signature']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session_completed(session)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_invoice_payment_succeeded(invoice)

    return HttpResponse(status=200)

def handle_checkout_session_completed(session):
    subscription = Subscription.objects.get(selected_subscription_id=session['line_items'][0]['price']['id'])
    subscription.status = 'paid'
    subscription.save()

def handle_invoice_payment_succeeded(invoice):
    subscription = Subscription.objects.get(selected_subscription_id=invoice['lines']['data'][0]['price']['id'])
    subscription.status = 'paid'
    subscription.save()