#apps/StripePayment/models.py
from django.db import models
from decimal import Decimal
from django.conf import settings

 
class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
 
class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def get_display_price(self):
        return "{0:.2f}".format(self.price)
    

class Donation(models.Model):
    #DONATION_TYPES = (
      #  ('one-off', 'One-off'),
     #   ('monthly', 'Monthly Subscription'),
    #)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    #donation_type = models.CharField(max_length=10, choices=DONATION_TYPES)
    stripe_checkout_session_id = models.CharField(max_length=100, blank=True, null=True)
    completed = models.BooleanField(default=False)
    checkout_status = models.CharField(max_length=20, blank=True, null=True)  # New field

   # subscription_plan_id = models.CharField(max_length=100, blank=True, null=True)
   # subscription_start_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return "${0:.2f}".format(self.amount)
    

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    subscription_plan_id = models.CharField(max_length=100, unique=True)
    stripe_checkout_session_id = models.CharField(max_length=100)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    checkout_status = models.CharField(max_length=20, blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan_id}"
