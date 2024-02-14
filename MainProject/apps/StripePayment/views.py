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
from StripePayment.utils import get_or_create_stripe_customer_id


 
stripe.api_key = settings.STRIPE_SECRET_KEY
 


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
    


    def get(self, request, *args, **kwargs):
        get_or_create_stripe_customer_id(request.user)
        subscription_info = self.get_subscription_info(request)
        user_subscribed = self.is_user_subscribed(request.user)  # Replace with your logic to check if the user is subscribed
        user_subscription_name = self.get_user_subscription_name(request.user)
        # Pass the information to the template context
        context = {
            'subscription_info': subscription_info,
            'user_subscribed': user_subscribed,
            'user_subscription_name': user_subscription_name,
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Set the Stripe secret key

        try:

            plan_id = request.POST.get('plan_id')  # Assuming a form field for subscription plan selection
            # Check if the user already has an active subscription
            existing_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

            if existing_subscription:
                # User already has an active subscription, handle accordingly
                messages.warning(request, 'You are already subscribed to a plan.')
                return redirect('subscription_list')  # Change to your actual subscription list URL


            # Retrieve the prices using the Stripe API
            prices = stripe.Price.list(active=True, limit=10)  # Limit can be adjusted as needed
            price_ids = [price.id for price in prices.data]

            if plan_id not in price_ids:
                raise ValueError("Invalid plan selected")


            domain = "https://thewildernet.com"  # Default to thewildernet.com

            # Redirect www version to non-www if accessing through www
            if 'www.' in request.META.get('HTTP_HOST'):
                return redirect("https://thewildernet.com" + request.get_full_path(), permanent=True)

            # Adjust domain if in debug mode
            if settings.DEBUG:
                domain = "http://127.0.0.1:8000"  # Replace with your debug domain

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                subscription_data={
                    'items': [{
                        'price': plan_id,  # Use the selected price ID directly
                        'quantity': 1,
                    }]
                },
                mode='subscription',
                success_url=domain + '/subscription-success/',
                cancel_url=domain + '/subscription-cancel/',
            )
            

            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            return render(request, self.template_name, {'error': str(e)})
        except ValueError as e:
            # Handle invalid plan ID error
            return render(request, self.template_name, {'error': str(e)})




class CreateSubscriptionCheckoutSessionView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        get_or_create_stripe_customer_id(request.user)
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
        subscription_amount = float(price.unit_amount_decimal) / 100  # Convert to integer and then divide by 100

        product = stripe.Product.retrieve(price.product)
        product_name = product.name if hasattr(product, 'name') else "Unknown Product"


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

        # Create a new Subscription instance only if there is no existing active subscription
        if not existing_subscription:
            subscription = Subscription(
                user=user,
                amount=subscription_amount,
                subscription_plan_id=plan_id,
                stripe_checkout_session_id=checkout_session.id,
                is_active=True,
                product=Product.objects.get_or_create(name=product_name)[0],  # Create or get the product
                stripe_customer_id=user.stripe_customer_id if user else None,

                # Add more subscription-related fields as needed
            )
            subscription.save()

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



class CancelSubscriptionView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Get the user's subscription
            user_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
            #print(user_subscription)
            #print(user_subscription.stripe_subscription_id)
            if user_subscription and user_subscription.stripe_subscription_id:
                # Cancel the subscription using the Stripe API
                stripe.Subscription.modify(
                    user_subscription.stripe_subscription_id,
                    cancel_at_period_end=False  # This will cancel immediately
                )

                # Update the local database to mark the subscription as canceled
                user_subscription.is_active = False
                user_subscription.save()

                messages.success(request, 'Your subscription has been canceled.')
                return redirect('StripePayment:subscription_cancelled')
            elif not user_subscription:
                messages.warning(request, 'You are not currently subscribed.')
            else:
                messages.warning(request, 'Unable to cancel subscription. Please contact support.')

        except StripeError as e:
            messages.error(request, f'Stripe Error: {str(e)}')

        return redirect('StripePayment:subscription_cancelled')  # Redirect to the donation page or another appropriate page

class SubscriptionCancelledView(View):
    template_name = "StripePayment/subscription_cancelled.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ManageSubscriptionView(View):
    template_name = "manage_subscription.html"

    def get(self, request, *args, **kwargs):
        try:
            # Retrieve the active subscription for the user
            subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

            if subscription and subscription.stripe_customer_id:
                # If the subscription and customer ID are available, proceed with creating the session
               #session = stripe.billing_portal.Session.create(
                #    customer=subscription.stripe_customer_id,
                 #   return_url=settings.STRIPE_BILLING_RETURN_URL,
                 
                #)
                #return redirect(session.url)
                if settings.DEBUG:
                    billing_portal_link = f"https://billing.stripe.com/p/login/test_28o3cH49MbO52JydQR"
                else:
                    billing_portal_link = f"https://billing.stripe.com/p/login/3cs4gk1Eaffo2E87ss"
                return redirect(billing_portal_link)
            else:
                # Handle the case where the subscription or customer ID is missing
                error_message = "Subscription or customer ID not found."
                messages.error(request, error_message)
                return redirect(reverse('StripePayment:error', kwargs={'error_message': error_message}))

        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            error_message = f'Stripe Error: {str(e)}'
            messages.error(request, error_message)
            return redirect(reverse('StripePayment:error', kwargs={'error_message': error_message}))



def error_view(request, error_message="An unexpected error occurred."):
    return render(request, 'error.html', {'error_message': error_message})

@csrf_exempt
def stripe_webhook(request):
    print("Webhook triggered!")  # Add this print statement

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.DJSTRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Check if it's a one-time payment (donation)
        if 'payment_intent' in session:
            amount_paid = session['amount_total']
            customer_email = session['customer_details']['email']
            # Handle donation logic (e.g., send a thank-you email)
            send_mail(
                subject="Thank You for Your Donation",
                message=f"Thank you for donating ${amount_paid / 100}. Your support is appreciated!",
                recipient_list=[customer_email],
                from_email="contact.jidder@gmail.com"
            )
        else:
            # It's a subscription payment
            customer_email = session["customer_details"]["email"]
            line_items = stripe.checkout.Session.list_line_items(session["id"])
            stripe_checkout_session_id = session["subscription"]


            stripe_price_id = line_items["data"][0]["price"]["id"]
            price = Price.objects.get(stripe_price_id=stripe_price_id)
            existing_subscription = Subscription.objects.filter(
                stripe_checkout_session_id=stripe_checkout_session_id
            )
            if existing_subscription:
                # Handle subscription logic
                send_mail(
                    subject="Thank You for Your Subscription",
                    message=f"Thank you for subscribing ${price}/month. Your support is appreciated!",
                    recipient_list=[customer_email],
                    from_email="contact.jidder@gmail.com"
                )
                existing_subscription.completed = True
                existing_subscription.save()

    return HttpResponse(status=200)
