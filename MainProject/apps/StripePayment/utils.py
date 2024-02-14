# apps/StripePayment/utils.py

import stripe
from django.conf import settings
from .models import Subscription, Product 

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_or_create_stripe_customer_id(user):
    """
    Check if the user has a stripe_customer_id. If not, create a new customer on Stripe
    and associate the customer ID with the user.
    """
    stripe_customer_id = getattr(user, 'stripe_customer_id', None)

    if not stripe_customer_id:
        try:
            # Create a new customer on Stripe
            customer = stripe.Customer.create(
                email=user.email,
               
                # You can include additional parameters if needed
            )

            # Update the user model with the stripe_customer_id
            user.stripe_customer_id = customer.id
            user.save()

            return customer.id
        except stripe.error.StripeError as e:
            # Handle the error appropriately (log, display a message, etc.)
            print(f'Stripe Error: {str(e)}')
            return None
    else:
        return stripe_customer_id
