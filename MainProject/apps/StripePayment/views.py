#apps/StripePayment/views.py
import stripe
from .models import Price, Product
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.generic import TemplateView
 

 
stripe.api_key = settings.STRIPE_SECRET_KEY
 
 
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
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
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)



class ProductLandingPageView(TemplateView):
    template_name = "StripePayment/landing.html"
 
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        context = super(ProductLandingPageView,
                        self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context

class SuccessView(TemplateView):
    template_name = "StripePayment/success.html"
 
class CancelView(TemplateView):
    template_name = "StripePayment/cancel.html"




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
            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            # Handle the exception appropriately (e.g., show an error message)
            return render(request, self.template_name, context={'error_message': str(e)})





class DonationSuccessView(TemplateView):
    template_name = "StripePayment/donation_success.html"
 
class DonationCancelView(TemplateView):
    template_name = "StripePayment/donation_cancel.html"


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
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
                from_email="your@email.com"
            )
        else:
            # It's a subscription payment
            customer_email = session["customer_details"]["email"]
            line_items = stripe.checkout.Session.list_line_items(session["id"])
            stripe_price_id = line_items["data"][0]["price"]["id"]
            price = Price.objects.get(stripe_price_id=stripe_price_id)
            product = price.product
            # Handle subscription logic (e.g., send subscription confirmation email)
         

    return HttpResponse(status=200)



#This

class SubscriptionView(View):
    template_name = "StripePayment/subscription.html"

    def get(self, request, *args, **kwargs):
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
                            'name': product.name,
                            'price': "{:.2f}".format(price_amount)
                        })

            return render(request, self.template_name, {'subscription_info': subscription_info})

        except stripe.error.StripeError as e:
        # Handle Stripe API errors
            return render(request, self.template_name, {'error': str(e)})


    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Set the Stripe secret key

        try:
            plan_id = request.POST.get('plan_id')  # Assuming a form field for subscription plan selection

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
    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get('plan_id')  # Assuming the plan_id is sent from the form
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
                    'price': plan_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=domain + '/subscription-success/',
            cancel_url=domain + '/subscription-cancel/',
        )
        return redirect(checkout_session.url)
    


class SubscriptionSuccessView(TemplateView):
    template_name = "StripePayment/subscription_success.html"
 
class SubscriptionCancelView(TemplateView):
    template_name = "StripePayment/subscription_cancel.html"