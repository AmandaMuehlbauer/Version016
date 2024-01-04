#apps/StripePayment/models.py
from django.db import models
from decimal import Decimal
 
 
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
    DONATION_TYPES = (
        ('one-off', 'One-off'),
        ('monthly', 'Monthly Subscription'),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    donation_type = models.CharField(max_length=10, choices=DONATION_TYPES)

    def __str__(self):
        return "${0:.2f}".format(self.amount)