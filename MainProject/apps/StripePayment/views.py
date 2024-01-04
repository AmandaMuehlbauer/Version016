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
        domain = "https://jidder.onrender.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
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
            domain = "https://jidder.onrender.com"
            if settings.DEBUG:
                domain = "http://127.0.0.1:8000"
                
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
 
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        line_items = stripe.checkout.Session.list_line_items(session["id"])
 
        stripe_price_id = line_items["data"][0]["price"]["id"]
        price = Price.objects.get(stripe_price_id=stripe_price_id)
        product = price.product

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase.",
                recipient_list=[customer_email],
                from_email="your@email.com"
        )

    
        
 
    return HttpResponse(status=200)

