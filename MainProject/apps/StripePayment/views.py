import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Price, Product
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail

 
stripe.api_key = settings.STRIPE_SECRET_KEY
 
 
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        domain = "https://yourdomain.com"
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


from django.views.generic import TemplateView
 
 
class SuccessView(TemplateView):
    template_name = "StripePayment/success.html"
 
class CancelView(TemplateView):
    template_name = "StripePayment/cancel.html"


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


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            price = Price.objects.get(id=self.kwargs["pk"])
            intent = stripe.PaymentIntent.create(
                amount=price.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "price_id": price.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
        


class CustomPaymentView(TemplateView):
    template_name = "StripePayment/custom_payment.html"
 
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        prices = Price.objects.filter(product=product)
        context = super(CustomPaymentView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context