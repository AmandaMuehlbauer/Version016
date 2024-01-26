#apps/StripePayment/views.py
import stripe
from .models import Price, Product, Donation, Subscription
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.users.models import User

 

 
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

            # Check if the user already has an active subscription
            if request.user.is_authenticated:
                existing_subscription = Subscription.objects.filter(user=User.objects.get(pk=request.user.pk), is_active=True).first()

                if existing_subscription:
                    subscription_info.append({
                        'id': existing_subscription.subscription_plan_id,
                        'name': existing_subscription.subscription_plan_id,
                        'price': "{:.2f}".format(existing_subscription.amount),
                        'is_active': True,
                    })
                
                else:
                    print("user is not authemticated")

            prices = stripe.Price.list(active=True, limit=10).data  # Retrieve subscription prices

            for price in prices:
                if price.type == 'recurring':
                    product = stripe.Product.retrieve(price.product)
                    if hasattr(product, 'name'):
                        price_amount = float(price.unit_amount_decimal) / 100  # Convert to integer and then divide by 100

                        subscription_info.append({
                            'id': price.id,  # Include the price ID
                            'name': product.name,
                            'price': "{:.2f}".format(price_amount),
                            'is_active': False,
                        })

            return subscription_info

        except stripe.error.StripeError as e:
        # Handle Stripe API errors
            return []    
        
    def get(self, request, *args, **kwargs):
        subscription_info = self.get_subscription_info()

        return render(request, self.template_name, {'subscription_info': subscription_info})


    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Set the Stripe secret key

        try:
            plan_id = request.POST.get('plan_id')  # Assuming a form field for subscription plan selection


            # Check if the user already has an active subscription
            existing_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

            if existing_subscription:
                # User wants to switch the plan
                existing_subscription.is_active = False
                existing_subscription.save()

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

    def unsubscribe(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user, is_active=True)

            if subscription.stripe_subscription_id:
                # Make API call to Stripe to cancel the subscription
                stripe.Subscription.delete(subscription.stripe_subscription_id)

            subscription.is_active = False
            subscription.save()
            messages.success(request, 'Subscription unsubscribed successfully.')
        except Subscription.DoesNotExist:
            messages.error(request, 'Subscription not found or already unsubscribed.')
        return redirect('your_subscription_list_view')

        


class CreateSubscriptionCheckoutSessionView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get('plan_id')  # Assuming the plan_id is sent from the form
        domain = "https://thewildernet.com"  # Default to thewildernet.com

            # Redirect www version to non-www if accessing through www
        if 'www.' in request.META.get('HTTP_HOST'):
            return redirect("https://thewildernet.com" + request.get_full_path(), permanent=True)

            # Adjust domain if in debug mode
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"  # Replace with your debug domain

        price = stripe.Price.retrieve(plan_id)
        subscription_amount = float(price.unit_amount_decimal) / 100  # Convert to integer and then divide by 100


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

            # Create a new Donation instance with subscription-related information
        subscription = Subscription(
            user=request.user,  # Assuming request.user represents the authenticated user
            amount=subscription_amount,  # Set the amount as needed, it can be 0 for subscription
            subscription_plan_id=plan_id,  # Store the subscription plan ID
            stripe_checkout_session_id=checkout_session.id,
            is_active=True,

                # Add more subscription-related fields as needed
            )
        subscription.save()
        return redirect(checkout_session.url)
    


class SubscriptionSuccessView(TemplateView):
    template_name = "StripePayment/subscription_success.html"
 
class SubscriptionCancelView(TemplateView):
    template_name = "StripePayment/subscription_cancel.html"



class CombinedView(View):
    template_name = "StripePayment/donate.html"
    

    def get_donation_info(self):
        # Fetch donation information
        # This assumes DonationView has a method get_donation_info()
        donation_view = DonationView()
        return donation_view.get_donation_info()

    def get_subscription_info(self, request):
        # Fetch subscription information
        # This assumes SubscriptionView has a method get_subscription_info()
        subscription_view = SubscriptionView()
        return subscription_view.get_subscription_info(request)

    def get(self, request, *args, **kwargs):
        donation_info = self.get_donation_info()
        subscription_info = self.get_subscription_info(request)

        # Check if subscription_info is not empty before rendering the template
        if not subscription_info:
            subscription_info = []  # Set it to an empty list to avoid template errors


        context = {
            'donation_info': donation_info,
            'subscription_info': subscription_info,
        }

        return render(request, self.template_name, context)
    

#View for user to check their subscription
class SubscriptionListView(View):
    template_name = "StripePayment/subscription_list.html"

    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(user=request.user, is_active=True)
        context = {'subscriptions': subscriptions}
        return render(request, self.template_name, context)
    

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
