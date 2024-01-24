#apps/StripePayment/admin.py
from django.contrib import admin
from .models import Product, Price, Donation
 
 
class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0
 

class DonationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'donation_type', 'stripe_checkout_session_id', 'subscription_plan_id', 'subscription_start_date']
    search_fields = ['amount', 'donation_type']
    list_filter = ['donation_type']
 
class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]
 
 
admin.site.register(Product, ProductAdmin)
admin.site.register(Donation, DonationAdmin)
