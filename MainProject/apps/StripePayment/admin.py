from django.contrib import admin
from .models import Product, Price, Donation, Subscription

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stripe_product_id']
    inlines = [PriceInlineAdmin]

    def prices(self, obj):
        return ', '.join([str(price) for price in obj.price_set.all()])
    prices.short_description = 'Prices'

admin.site.register(Product, ProductAdmin)

class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'stripe_checkout_session_id', 'completed', 'checkout_status', 'stripe_customer_id']  
    search_fields = ['user__username', 'amount', 'stripe_checkout_session_id']
    list_filter = ['completed', 'checkout_status']

admin.site.register(Donation, DonationAdmin)

class SubscriptionPriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','amount', 'subscription_plan_id', 'stripe_checkout_session_id', 'created_at', 'is_active', 'completed', 'checkout_status', 'stripe_customer_id']  # Add 'stripe_customer_id'
    search_fields = ['user__username', 'amount', 'subscription_plan_id', 'stripe_checkout_session_id']
    list_filter = ['is_active', 'completed', 'checkout_status']

admin.site.register(Subscription, SubscriptionAdmin)
